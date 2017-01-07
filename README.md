# Cabot Facebook Messenger Plugin

This is an alert plugin for Cabot. It allows you to alert users on Facebook Messenger.

## Installation


Inside the Cabot virtual environment, install this plugin using pip

```
pip install git+https://github.com/tjphopkins/cabot-alert-fbmessenger.git
```

If using default deployment methodology (via fab deploy):
Edit conf/production.env in your Cabot clone to include the plugin and the version number:

If isntead you are using docker you will need to run:
```
docker-compose run --rm web python manage.py syncdb
```

CABOT_PLUGINS_ENABLED=cabot_alert_hipchat>=0.0.2,...,<other plugins>
```
Run fab deploy -H ubuntu@yourserver.example.com
```
(see http://cabotapp.com/qs/quickstart.html for more information).

The CABOT_PLUGINS_ENABLED environment variable triggers both installation of the plugin (via Cabot's setup.py file) and inclusion in INSTALLED_APPS.

I
