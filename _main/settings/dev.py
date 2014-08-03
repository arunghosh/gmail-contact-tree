__author__ = 'lenovo'

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

GMAIL_CLIENT_ID = '864339645094-6u7141gbiprre8u1r122e1tjkghk7ev9.apps.googleusercontent.com'
GMAIL_CLIENT_SECRET = 'wlX4AGzMC1YIS_aQdptABlJ2'
GMAIL_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/plus.me email'
GMAIL_REDIRECT_URI = 'http://localhost:9000/oauth2callback'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'contact_db',
        'USER': 'postgres',
        'PASSWORD': 'abcd1234',
        'OPTIONS': {
            "autocommit": True,
        },
    }
}