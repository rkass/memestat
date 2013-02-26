from django.conf.urls import patterns, include, url
from memestat.views import home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  ('^$', home),
)

urlpatterns += staticfiles_urlpatterns()
