# Cabot Facebook Messenger Plugin

This is an alert plugin for Cabot. It allows you to alert users on Facebook Messenger.

## Installation

In the Cabot virtual environment, run
```
pip install git+https://github.com/tjphopkins/cabot-alert-fbmessenger.git
```

Then run `stop cabot` and modify the CABOT_PLUGINS_ENABLED environment variable
in conf/\<env\>.env to include the plugin:
```
CABOT_PLUGINS_ENABLED=cabot_alert_fbmessenger,...,<other plugins>
```

You should also add your FB_MESSENGER_PAGE_ACCESS_TOKEN to conf/\<env\>.env
at this point.

Then run:
```
foreman run -e conf/production.env python manage.py syncdb
start cabot
```
