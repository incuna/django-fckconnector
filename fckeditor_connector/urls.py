from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',

    (r'^browser/$', 'fckeditor_connector.views.browser'),
    (r'^uploader/$', 'fckeditor_connector.views.uploader'),

                       )
