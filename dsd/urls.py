from django.conf.urls import url

from dsd.api.indicator_endpoint import indicator_endpoint
from . import views

urlpatterns = [
    url(r'^api/indicator/', indicator_endpoint, name="indicator"),
    url(r'^$', views.index, name='index'),
]
