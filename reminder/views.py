from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from common.views import JSONResponseMixin
from django.views.generic.base import View
import json


class AddReminder(JSONResponseMixin, APIView):

    def post(self, request):
        data = json.loads(request.POST)
        cid = data.get('cid')
        date = data.get('date')
