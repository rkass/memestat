from django.conf.urls import patterns, include, url
from memestat.views import home

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  ('^$', home),
)
