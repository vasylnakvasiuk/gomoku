# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


class RoundAdmin(admin.ModelAdmin):
    list_display = ('creator', 'opponent', 'dimension', 'lineup')
admin.site.register(models.Round, RoundAdmin)


class PlayerPositionAdmin(admin.ModelAdmin):
    list_display = ('player', 'wins', 'losses', 'draws')
admin.site.register(models.PlayerPosition, PlayerPositionAdmin)
