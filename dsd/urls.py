from django.conf.urls import url

from dsd.api.completeness_selection import data_completeness_endpoint
from dsd.api.indicator_endpoint import indicator_endpoint
from . import views

urlpatterns = [
    url(r'^api/indicator/', indicator_endpoint, name="indicator"),
    url(r'^api/data_completeness', data_completeness_endpoint, name='data_freshness'),
    url(r'^$', views.index, name='index'),
]
