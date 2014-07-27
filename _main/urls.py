from django.conf.urls import patterns, include, url

from django.contrib import admin
from auth.views import login
from gmail.views import login as gmail_login, callback
from inbox.views import ContactsView, MailListView, RecentMailsView
from manager.views import ContactsWithZoneView, UpdateFollowStatus, home, RefreshInboxView, ImportInboxView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, name='login'),
    url(r'^gmail/$', gmail_login),
    url(r'^oauth2callback/$', callback),
    url(r'^contacts/$', ContactsView.as_view()),
    # url(r'^date_map/$', DateMapView.as_view()),
    url(r'^$', home),
    url(r'^by_zone/$', ContactsWithZoneView.as_view()),
    url(r'^refresh_inbox/$', RefreshInboxView.as_view()),
    url(r'^import_inbox/$', ImportInboxView.as_view()),
    url(r'^recent_mails/$', RecentMailsView.as_view()),
    url(r'^update_status/(?P<cid>[0-9]*)/(?P<status>[0-9]*)/$', UpdateFollowStatus.as_view()),
    url(r'^mails/(?P<cid>[0-9]*)/$', MailListView.as_view()),
)
