from django.conf.urls import url

from dsd.api.sync_status_endpoint import SyncStatusList
from . import views

urlpatterns = [
    url(r'^api/sync-status/', SyncStatusList.as_view(), name="sync_status"),
    url(r'^$', views.index, name='index'),
]
