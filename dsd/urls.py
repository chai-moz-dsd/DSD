from django.conf.urls import url

from dsd.api.sync_status_endpoint import sync_status
from . import views

urlpatterns = [
    url(r'^api/sync-status/', sync_status, name="sync_status"),
    url(r'^$', views.index, name='index'),
]
