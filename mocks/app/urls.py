from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login$', 'app.views.mlogin'),
    url(r'^register$', 'app.views.mregister'),
    # url(r'^logout$', 'app.views.logout'),

    url(r'^$', 'app.views.home'),
    # url(r'^scheduled$', 'app.views.scheduled'),
)
