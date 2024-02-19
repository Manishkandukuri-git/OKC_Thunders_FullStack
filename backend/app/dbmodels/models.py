# -*- coding: utf-8 -*-
"""Contains models related to stats"""
from django.db import models
# appname/models.py
from django.db import models

# appname/models.py
# appname/models.py
from django.db import models

class Stats(models.Model):
    id = models.IntegerField(primary_key=True)
    is_starter = models.BooleanField()
    minutes = models.IntegerField()
    points = models.IntegerField()
    assists = models.IntegerField()
    offensive_rebounds = models.IntegerField()
    defensive_rebounds = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    defensive_fouls = models.IntegerField()
    offensive_fouls = models.IntegerField()
    free_throws_made = models.IntegerField()
    free_throws_attempted = models.IntegerField()
    two_pointers_made = models.IntegerField()
    two_pointers_attempted = models.IntegerField()
    three_pointers_made = models.IntegerField()
    three_pointers_attempted = models.IntegerField()

    def __str__(self):
        return f"Player {self.id}"

class Shot(models.Model):
    shot_id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Stats, on_delete=models.CASCADE)
    is_make = models.BooleanField()
    location_x = models.FloatField()
    location_y = models.FloatField()

class Games(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    home_team = models.ForeignKey('Teams', related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey('Teams', related_name='away_games', on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Players(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# appname/models.py

class Teams(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
