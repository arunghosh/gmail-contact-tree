from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from auth.views import login, logout_user
from contact.views import UpdateMobile, UpdateCtgry, UpdateFollowStatus, CommItemsView, MonthView, UpdateNote
from gmail.views import login as gmail_login, callback, RefreshInboxView, ImportInboxView
from inbox.views import  MailListView, RecentMailsView
from manager.views import ContactsWithZoneView, home, UserInfo, DuplicateContacts, MergeContacts
from mobile.views import GetUserIdForMobView, UpdateCallsView, RecentCallsView, CallListView, GetLastUpdated
from lkdn.views import ln_callback, ln_home, DuplicateLnContacts
from zone.views import ZoneTimeView, RemovedCategories, ToggleCategory
from reminder.views import AddReminder, Reminders, DeleteReminder, AllReminders

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout_user),
    url(r'^update_mobile/(?P<mobile>[0-9]*)/$', UpdateMobile.as_view()),
    url(r'^user_info/$', UserInfo   .as_view()),

    url(r'^contacts/$', ContactsWithZoneView.as_view()),
    url(r'^contact/status/(?P<cid>[0-9]*)/(?P<status>[0-9]*)/$', UpdateFollowStatus.as_view()),
    url(r'^contact/note/(?P<cid>[0-9]*)/$', UpdateNote.as_view()),
    url(r'^contact/ctgry/(?P<cid>[0-9]*)/(?P<ctgry>\w+)/$', UpdateCtgry.as_view()),
    url(r'^contact/duplicates/(?P<cid>[0-9]*)/$', DuplicateContacts.as_view()),
    url(r'^contacts/merge/$', MergeContacts.as_view()),
    url(r'^contact/comm_items/(?P<cid>[0-9]*)/$', CommItemsView.as_view()),
    url(r'^contact/by_month/(?P<cid>[0-9]*)/$', MonthView.as_view()),

    url(r'^reminders/$', AllReminders.as_view()),
    url(r'^reminder/add/$', AddReminder.as_view()),
    url(r'^reminder/delete/$', DeleteReminder.as_view()),
    url(r'^contact/reminders/(?P<cid>[0-9]*)/$', Reminders.as_view()),

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
    url(r'^mobile/last_update/$', GetLastUpdated.as_view()),

    url(r'^setting/zones/$', ZoneTimeView.as_view()),
    url(r'^rcategory/toggle/$', ToggleCategory.as_view()),
    url(r'^rcategorys/$', RemovedCategories.as_view()),
    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# static files (images, css, javascript, etc.)
# urlpatterns += patterns('',
#                         (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#                             'document_root': settings.STATIC_ROOT}))