from django.shortcuts import render
from common.views import JSONResponseMixin
from django.views.generic.base import View
import json
# Create your views here.


class ZoneTimeView(JSONResponseMixin, View):

    def get(self, request):
        user = request.user
        return self.render_json_response({'p1': user.delta_safe, 'p2': user.delta_danger})

    def post(self, request):
        user = request.user
        data = json.loads(request.read())
        user.delta_safe = data['p1']
        user.delta_danger = data['p2']
        user.save()
        return self.render_json_response({'status': True})