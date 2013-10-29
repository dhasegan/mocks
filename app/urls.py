from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login$', 'app.views.mlogin', name='login'),
    url(r'^register$', 'app.views.mregister', name='register'),
    url(r'^logout$', 'app.views.mlogout', name='logout'),
    url(r'^confirm-registration/(?P<emailId>[\w\.0-9\@\%\-\.]+)/(?P<token>[a-z0-9\-]+)$', 'app.views.confirm_registration', name='confirmEmail'),

    url(r'^$', 'app.views.home'),
    url(r'^home$', 'app.views.home', name='home'),
    url(r'^createslot$', 'app.views.createslot'),
    url(r'^schedule$', 'app.views.schedule'),
    url(r'^profile$', 'app.views.profile'),
    url(r'^profile-change$', 'app.views.profilechange'),
    url(r'^password-change$', 'app.views.passwordchange'),

    url(r'^info/(?P<interviewId>[0-9]+)$', 'app.views.scheduleInterview', name='info'),
    url(r'^delete/(?P<interviewId>[0-9]+)$', 'app.views.deleteInterview', name='delete'),

    url(r'^about$', 'app.views.about'),
    url(r'^feedback$', 'app.views.feedback'),
)