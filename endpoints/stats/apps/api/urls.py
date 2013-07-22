# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^round/save$', 'apps.api.views.round_save', name='round_save'),
    url(r'^player/top$', 'apps.api.views.player_top', name='player_top'),
)
