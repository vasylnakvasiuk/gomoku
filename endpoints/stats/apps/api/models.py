# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Round(models.Model):
    creator = models.ForeignKey(
        User, verbose_name='Creator of the round', related_name='creator_rounds')
    opponent = models.ForeignKey(
        User, verbose_name='Opponent', related_name='opponent_rounds')
    dimension = models.IntegerField(
        'Dimension', default=3,
        validators=[MinValueValidator(3)])
    lineup = models.IntegerField(
        'Line Up', default=3,
        validators=[MinValueValidator(3)])
    black_stone_owner = models.ForeignKey(
        User, verbose_name='Black stone owner', related_name='black_stone_rounds')
    moves = models.IntegerField('Moves')
    winner = models.ForeignKey(
        User, verbose_name='Winner', related_name='win_rounds',
        blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return '{0}x{0} ({1})'.format(self.dimension, self.lineup)

    class Meta:
        verbose_name = 'Round'
        verbose_name_plural = 'Rounds'
