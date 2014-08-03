from .base import *

import dj_database_url


DEBUG = False

GMAIL_CLIENT_ID = '864339645094-rii2aqr2jm20k63hf6jjt2pr7c6qku31.apps.googleusercontent.com'
GMAIL_CLIENT_SECRET = 'nT3ebkSkWSUGdob-yfxNdCGC'
GMAIL_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/plus.me email'
GMAIL_REDIRECT_URI = 'http://rdtcontactapp.herokuapp.com/oauth2callback'

DATABASES = {'default': dj_database_url.config()}

