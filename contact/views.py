from django.shortcuts import render
from common.views import JSONResponseMixin
from django.views.generic.base import View
from .models import UserContact


class UpdateFollowStatus(JSONResponseMixin, View):

    def post(self, request, cid, status):
        c = UserContact.objects.get(pk=cid)
        c.status = status
        c.save()
        return self.render_json_response({})


class UpdateMobile(JSONResponseMixin, View):

    def post(self, request, mobile):
        user = request.user
        user.phone = mobile
        print mobile
        user.save()
        return self.render_json_response({'status':True})


class UpdateCtgry(JSONResponseMixin, View):

    def post(self, request, cid, ctgry):
        c = UserContact.objects.get(pk=cid)
        c.category = ctgry
        c.save()
        return self.render_json_response({'status':True})