import requests
from requests.exceptions import RequestException
import logging
import re

from django.db import models
from django.template import Context, loader
from django.conf import settings
from django.core.exceptions import ValidationError

from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

from os import environ as env

logger = logging.getLogger('FacebookMessengerAlertPlugin.send_alert')


def _validate_fb_mobile_number(fb_mobile_number):
    pattern = re.compile("^\+[1-9]{1}?\([1-9]{3}\)[1-9]{3}-[1-9]{4}")
    result = pattern.findall(fb_mobile_number)
    if len(result) == 1:
        return
    raise ValidationError(
        "The fb_mobile_number entered is invalid. It must be in the"
        " format +1(212)555-2368")


class FacebookMessengerAlertUserData(AlertPluginUserData):
    name = "Facebook Messenger"
    # This mobile number may be different to the user's primary number
    # used for SMS and phone call alerts.
    fb_mobile_number = models.CharField(max_length=30, blank=True)

    def save(self, *args, **kwargs):
        # The phone number must be in the format +1(212)555-2368
        # TODO: Ensure ValidationError is raised to client
        _validate_fb_mobile_number(self.fb_mobile_number)
        return super(FacebookMessengerAlertUserData, self).save(*args, **kwargs)


class FacebookMessengerAlertPlugin(AlertPlugin):
    name = "Facebook Messenger"
    slug = "fbmessenger"
    author = "Thomas Hopkins"
    version = "0.0.3"

    def send_alert(self, service, users, duty_officers):
        """Send alert function to send alerts to users via Facebook Messenger

        :arg service object - cabotapp.models.Service instance
        :users list(object) - List of cabotapp.models.UserProfile instances
        :duty_officers list(object) - Subset of users that are currently on duty
        """
        if service.overall_status == service.WARNING_STATUS:
            return  # Don't alert at all for WARNING
        if service.overall_status == service.ERROR_STATUS and \
                service.old_overall_status == service.ERROR_STATUS:
            return  # Don't alert repeatedly for ERROR
        if service.overall_status == service.PASSING_STATUS and \
                service.old_overall_status == service.WARNING_STATUS:
            # Don't alert for recovery from WARNING status
            return

        # I assume here that users are all users subscribed to this service.
        # Unfortunately the documentation is truncated at the point where it
        # describes the arguments passed to send_alert.
        phone_numbers = [
            u.fb_mobile_number for u in
            FacebookMessengerAlertUserData.objects.filter(user__user__in=users)]

        template = loader.get_template('message_template.txt')
        context = Context({
            'service': service,
            'host': settings.WWW_HTTP_HOST,
            'scheme': settings.WWW_SCHEME,
        })
        message = template.render(context)

        access_token = env.get('FB_MESSENGER_PAGE_ACCESS_TOKEN')
        url = "https://graph.facebook.com/v2.6/me/messages?access_token={t}"\
            .format(t=access_token)

        # TODO: Use urllib3 as opposed to requests for better retry and error
        # handling. It would also be sensible to attempt every number before
        # making any retries.
        for number in phone_numbers:
            self._send_alert_to_number(url, number, message)

    def _send_alert_to_number(self, url, number, message):
        try:
            res = requests.post(
                url, data={'message': {'text': message},
                           'recipient': {'phone_number': number}}
            )
            res.raise_for_status()
        except RequestException as e:
            logger.exception(
                'Error sending message to number {n}: {e}'
                .format(n=number, e=e))
