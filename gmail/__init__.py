from oauth2client.client import OAuth2WebServerFlow
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from auth.models import MyUser
from django.conf import settings


class Auth:

    flow = OAuth2WebServerFlow(
        client_id=settings.GMAIL_CLIENT_ID,
        client_secret=settings.GMAIL_CLIENT_SECRET,
        scope=settings.GMAIL_SCOPE,
        redirect_uri=settings.GMAIL_REDIRECT_URI)

    # flow = OAuth2WebServerFlow(
    #     client_id='864339645094-rii2aqr2jm20k63hf6jjt2pr7c6qku31.apps.googleusercontent.com',
    #     client_secret='nT3ebkSkWSUGdob-yfxNdCGC',
    #     scope='https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/plus.me email',
    #     redirect_uri='http://rdtcontactapp.herokuapp.com/oauth2callback')

    @staticmethod
    def get_auth_url():
        auth_uri = Auth.flow.step1_get_authorize_url()
        return auth_uri

    @staticmethod
    def __storage_file(user):
        return '_temp/credentials/' + user.email

    @staticmethod
    def get_auth_http(user):
        storage = Storage(Auth.__storage_file(user))
        credentials = storage.get()
        http = httplib2.Http()
        http = credentials.authorize(http)
        return http

    @staticmethod
    def get_gmail_srv(user):
        http = Auth.get_auth_http(user)
        return build('gmail', 'v1', http=http)

    @staticmethod
    def get_user_and_update_cred(code):
        credentials = Auth.flow.step2_exchange(code)
        http = httplib2.Http()
        http = credentials.authorize(http)

        service = build('plus', 'v1', http=http)
        response = service.people().get(userId='me').execute()
        user = MyUser()
        user.name = response['displayName']
        user.image_url = response['image']['url']
        user.email = response['emails'][0]['value']

        storage = Storage(Auth.__storage_file(user))
        storage.put(credentials)
        return user
