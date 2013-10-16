from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login$', 'app.views.mlogin', name='login'),
    url(r'^register$', 'app.views.mregister', name='register'),
    url(r'^logout$', 'app.views.mlogout', name='logout'),
    url(r'^confirm-registration/(?P<emailId>\w+)/(?P<token>[a-z0-9\-]+)$', 'app.views.confirm_registration', name='confirmEmail'),

    url(r'^$', 'app.views.home', name='home'),
    # url(r'^scheduled$', 'app.views.scheduled'),
)