# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^round/save$', 'apps.api.views.round_save', name='round_save'),
)
