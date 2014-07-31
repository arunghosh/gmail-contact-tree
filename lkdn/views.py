from django.shortcuts import render
from linkedin import linkedin
from django.http import HttpResponseRedirect
from django.db import transaction
from .parsers import ImportAll
from contact.models import UserContact
from rest_framework.response import Response
from rest_framework.views import APIView
from Levenshtein import ratio
from .models import LnContact
from .serializers import LnContactSerializer

API_KEY = 'rf2360q0zkme'
API_SECRET = 'EtY5qE7q4HvXggbr'
RETURN_URL = 'http://localhost:9000/lkdn/callback'
authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())


def ln_home(request):
    url = authentication.authorization_url  # open this url on your browser
    application = linkedin.LinkedInApplication(authentication)
    return HttpResponseRedirect(url)


@transaction.atomic
def ln_callback(request):
    user = request.user
    code = request.GET['code']
    authentication.authorization_code = code
    authentication.get_access_token()
    application = linkedin.LinkedInApplication(authentication)
    response = application.get_connections(selectors=['id', 'picture-url', 'public-profile-url', 'headline', 'first-name', 'last-name', 'email-address'])
    import_all = ImportAll(response, user)
    import_all.execute()
    return HttpResponseRedirect("/")


class DuplicateLnContacts(APIView):

    def get(self, request, cid):
        user = request.user
        c = UserContact.objects.get(pk=cid)
        name = c.name.lower()
        ln_contacts = [ln for ln in user.lncontact_set.all() if ratio(name, ln.name.lower()) > .76]
        slz = LnContactSerializer(ln_contacts, many=True)
        return Response(slz.data)