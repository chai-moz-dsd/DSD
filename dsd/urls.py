from django.conf.urls import url

from dsd.api.freshness_endpoint import freshness_status
from dsd.api.sync_status_endpoint import sync_status
from . import views

urlpatterns = [
    url(r'^api/sync-status/', sync_status, name="sync_status"),
    url(r'^api/freshness-status/', freshness_status, name="freshness_status"),
    url(r'^$', views.index, name='index'),
]
