from django.conf.urls import url

from dsd.api.completeness_selection import data_completeness_endpoint
from dsd.api.indicator_endpoint import indicator_endpoint
from dsd.api.message_endpoint import data_message_endpoint
from dsd.api.comments_endpoint import data_comments_endpoint
from . import views

urlpatterns = [
    url(r'^api/indicator/', indicator_endpoint, name="indicator"),
    url(r'^api/data_completeness', data_completeness_endpoint, name='data_freshness'),
    url(r'^api/data_message', data_message_endpoint, name='data_message'),
    url(r'^api/data_comments', data_comments_endpoint, name='data_comments'),
    url(r'^$', views.index, name='index'),
]
