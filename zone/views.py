from django.shortcuts import render
from common.views import JSONResponseMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic.base import View
import json

from .models import RemovedCategory
from .serializers import RemovedCtgrySerializer


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


class ToggleCategory(JSONResponseMixin, View):

    def post(self, request):
        user = request.user
        data = json.loads(request.read())
        ctgry = data['ctgry']
        ctgrys = [rc for rc in user.removedcategory_set.all() if rc.name == ctgry]
        if len(ctgrys) == 0:
            rc = RemovedCategory()
            rc.name = ctgry
            rc.user = user
            rc.save()
        else:
            ctgrys[0].delete()
        return self.get_json_response({'status': True})


class RemovedCategories(APIView):

    def get(self, request):
        user = request.user
        ctgrys = user.removedcategory_set.all()
        slz = RemovedCtgrySerializer(ctgrys)
        return Response(slz.data)

