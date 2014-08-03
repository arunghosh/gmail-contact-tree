from django.conf.urls import patterns, include, url

from django.contrib import admin
from auth.views import login
from contact.views import UpdateMobile, UpdateCtgry, UpdateFollowStatus
from gmail.views import login as gmail_login, callback, RefreshInboxView, ImportInboxView
from inbox.views import  MailListView, RecentMailsView
from manager.views import ContactsWithZoneView, home, UserInfo, DuplicateContacts, MergeContacts
from mobile.views import GetUserIdForMobView, UpdateCallsView, RecentCallsView, CallListView
from lkdn.views import ln_callback, ln_home, DuplicateLnContacts
from zone.views import ZoneTimeView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^login/$', login, name='login'),
    url(r'^update_mobile/(?P<mobile>[0-9]*)/$', UpdateMobile.as_view()),
    url(r'^user_info/$', UserInfo   .as_view()),

    # url(r'^contacts/$', ContactsView.as_view()),
    url(r'^contacts/$', ContactsWithZoneView.as_view()),
    url(r'^contact/status/(?P<cid>[0-9]*)/(?P<status>[0-9]*)/$', UpdateFollowStatus.as_view()),
    url(r'^contact/ctgry/(?P<cid>[0-9]*)/(?P<ctgry>\w+)/$', UpdateCtgry.as_view()),
    url(r'^contact/duplicates/(?P<cid>[0-9]*)/$', DuplicateContacts.as_view()),
    url(r'^contacts/merge/$', MergeContacts.as_view()),

    url(r'^gmail/$', gmail_login),
    url(r'^oauth2callback/$', callback),

    url(r'^lkdn/$', ln_home),
    url(r'^lkdn/callback/$', ln_callback),
    url(r'^lkdn/duplicates/(?P<cid>[0-9]*)/$', DuplicateLnContacts.as_view()),

    url(r'^inbox/refresh/$', RefreshInboxView.as_view()),
    url(r'^inbox/import/$', ImportInboxView.as_view()),
    url(r'^inbox/recent/$', RecentMailsView.as_view()),
    url(r'^inbox/mails/(?P<cid>[0-9]*)/$', MailListView.as_view()),

    url(r'^mobile/user_id/(?P<phone>[0-9]*)/$', GetUserIdForMobView.as_view()),
    url(r'^mobile/update/$', UpdateCallsView .as_view()),
    url(r'^mobile/recent/$', RecentCallsView.as_view()),
    url(r'^mobile/calls/(?P<cid>[0-9]*)/$', CallListView.as_view()),

    url(r'^setting/zones/$', ZoneTimeView.as_view()),

)
