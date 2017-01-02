from django.db import models
from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

from os import environ as env


class FacebookMessengerAlertUserData(AlertPluginUserData):
    name = "Facebook Messenger"
    fb_user_id = models.CharField(max_length=50, blank=True)


class SkeletonAlertPlugin(AlertPlugin):
    name = "Facebook Messenger"
    slug = "fbmessenger"
    author = "Thomas Hopkins"
    version = "0.0.1"

    def send_alert(self, service, users, duty_officers):
        return
