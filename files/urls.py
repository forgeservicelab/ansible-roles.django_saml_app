from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('',
    url(r'^saml2/', include('djangosaml2.urls')),
    url(r'^test/', 'djangosaml2.views.echo_attributes'),
    url(r'^$', views.index, name='index'),
)



