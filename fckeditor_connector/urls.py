from django.conf.urls.defaults import *

urlpatterns = patterns('',

    (r'^browser/$', 'fckeditor.connector.views.browser'),
    (r'^uploader/$', 'fckeditor.connector.views.uploader'),

                       )
