from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from . import views

class SimpleStaticView(TemplateView):
    def get_template_names(self):
        return [self.kwargs.get('template_name') + ".html"]

urlpatterns = [
    url(r'^', TemplateView.as_view(template_name='index_temp.html'), name='index'),
    url(r'^chai', TemplateView.as_view(template_name='chai_home.html'), name='chai_home'),
    url(r'^(?P<template_name>\w+)$', SimpleStaticView.as_view(), name='chai_template'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
