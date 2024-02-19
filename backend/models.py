# -*- coding: utf-8 -*-
"""Contains models related to stats"""
from django.db import models
# appname/models.py
from django.db import models

# appname/models.py
# appname/models.py
from django.db import models
import json

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

class Shot_Data(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    player = models.ForeignKey(Stats, on_delete=models.CASCADE)
    is_make = models.BooleanField(default=False)
    location_x = models.FloatField(default=0.0)
    location_y = models.FloatField(default=0.0)
    def __str__(self):
        return f"Player {self.id}"
# class Shot(models.Model):
#     id = models.AutoField(primary_key=True, unique=True)
#     player = models.ForeignKey(Stats, on_delete=models.CASCADE)
#     is_make = models.BooleanField()
#     location_x = models.FloatField()
#     location_y = models.FloatField()
#
#     def __str__(self):
#         return f"Player {self.id}"

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



class GamePlayer(models.Model):
    id = models.AutoField(primary_key=True)
    game_id = models.IntegerField()
    player_id = models.IntegerField()
    team_id = models.IntegerField()

    class Meta:
        unique_together = ('game_id', 'player_id', 'team_id')


# Load JSON teams data from a file
with open('raw_data/teams.json', 'r') as teams_file:
    teams_data = json.load(teams_file)

# Iterate over the JSON data and create model instances
for item in teams_data:
    teams_instance = Teams(
        id=item['id'],
        name=item['name'],
        # Add more fields as needed
    )
    teams_instance.save()

# Load JSON players data from a file
with open('raw_data/players.json', 'r') as players_file:
    players_data = json.load(players_file)

# Iterate over the JSON data and create model instances
for item in players_data:
    players_instance = Players(
        id=item['id'],
        name=item['name'],
        # Add more fields as needed
    )
    players_instance.save()



# Load JSON Games data from games.json file
with open('raw_data/games.json', 'r') as games_file:
    games_data = json.load(games_file)

# Iterate over the JSON data and create model instances
for item in games_data:
    games_instance = Games(
        id=item['id'],
        date=item['date'],
        away_team=Teams.objects.get(pk=item['awayTeam']['id']),
        home_team=Teams.objects.get(pk=item['homeTeam']['id']),
        # Add more fields as needed
    )
    games_instance.save()

# Load JSON Game_player data from games.json, players.json, teams.json file
with open('raw_data/games.json', 'r') as game_player_file:
    game_player_data = json.load(game_player_file)

# Iterate over the JSON data and create model instances
# for game in game_player_data:
#     home_team = Teams.objects.get(id=game['homeTeam']['id'])
#     away_team = Teams.objects.get(id=game['awayTeam']['id'])
#
#     for player_data in game['homeTeam']['players']:
#         player = Players.objects.get(id=player_data['id'])
#
#         # Create a GamePlayer instance for the home team
#         game_player_instance = GamePlayer(
#             game=Games.objects.get(id=game['id']),
#             player=player,
#             team=home_team,
#             # Add more fields as needed
#         )
#         game_player_instance.save()
#
#     for player_data in game['awayTeam']['players']:
#         player = Players.objects.get(id=player_data['id'])
#
#         # Create a GamePlayer instance for the away team
#         game_player_instance = GamePlayer(
#             game=Games.objects.get(id=game['id']),
#             player=player,
#             team=away_team,
#             # Add more fields as needed
#         )
#         game_player_instance.save()
# Iterate over the JSON data and create model instances
# for game in game_player_data:
#     for player in game['homeTeam']['players']:
#         game_player_instance = GamePlayer(
#             game_id=game['id'],
#             player_id=player['id'],
#             team_id=game['homeTeam']['id'],
#             # Add more fields as needed
#         )
#         game_player_instance.save()
#
#     for player in game['awayTeam']['players']:
#         game_player_instance = GamePlayer(
#             game_id=game['id'],
#             player_id=player['id'],
#             team_id=game['awayTeam']['id'],
#             # Add more fields as needed
#         )
#         game_player_instance.save()
#

# Load JSON Game_player data from games.json, players.json, teams.json file
with open('raw_data/games.json', 'r') as game_player_file:
    game_player_data = json.load(game_player_file)

for game in game_player_data:
    for player in game['homeTeam']['players']:
        game_id = game['id']
        player_id = player['id']
        team_id = game['homeTeam']['id']

        # Check if a record with the same combination already exists
        existing_record = GamePlayer.objects.filter(
            game_id=game_id,
            player_id=player_id,
            team_id=team_id
        ).first()

        if not existing_record:
            # No existing record found, create a new one
            game_player_instance = GamePlayer(
                game_id=game_id,
                player_id=player_id,
                team_id=team_id,
                # Add more fields as needed
            )
            game_player_instance.save()

# import json
# from myapp.models import Stats  # Import your Stats model from your Django app

# Load JSON Game data from the games.json file
with open('raw_data/games.json', 'r') as games_file:
    games_data = json.load(games_file)

# Iterate over the JSON data and create Stats model instances
for game_item in games_data:
    home_team_players = game_item['homeTeam']['players']
    away_team_players = game_item['awayTeam']['players']

    for player_data in home_team_players:
        # Create a Stats instance for the home team player
        stats_instance = Stats(
            id=player_data['id'],
            is_starter=player_data['isStarter'],
            minutes=player_data['minutes'],
            points=player_data['points'],
            assists=player_data['assists'],
            offensive_rebounds=player_data['offensiveRebounds'],
            defensive_rebounds=player_data['defensiveRebounds'],
            steals=player_data['steals'],
            blocks=player_data['blocks'],
            turnovers=player_data['turnovers'],
            defensive_fouls=player_data['defensiveFouls'],
            offensive_fouls=player_data['offensiveFouls'],
            free_throws_made=player_data['freeThrowsMade'],
            free_throws_attempted=player_data['freeThrowsAttempted'],
            two_pointers_made=player_data['twoPointersMade'],
            two_pointers_attempted=player_data['twoPointersAttempted'],
            three_pointers_made=player_data['threePointersMade'],
            three_pointers_attempted=player_data['threePointersAttempted'],
            # Add more fields as needed
        )
        stats_instance.save()

    # Create Stats instances for away team players
    for player_data in away_team_players:
        stats_instance = Stats(
            id=player_data['id'],
            is_starter=player_data['isStarter'],
            minutes=player_data['minutes'],
            points=player_data['points'],
            assists=player_data['assists'],
            offensive_rebounds=player_data['offensiveRebounds'],
            defensive_rebounds=player_data['defensiveRebounds'],
            steals=player_data['steals'],
            blocks=player_data['blocks'],
            turnovers=player_data['turnovers'],
            defensive_fouls=player_data['defensiveFouls'],
            offensive_fouls=player_data['offensiveFouls'],
            free_throws_made=player_data['freeThrowsMade'],
            free_throws_attempted=player_data['freeThrowsAttempted'],
            two_pointers_made=player_data['twoPointersMade'],
            two_pointers_attempted=player_data['twoPointersAttempted'],
            three_pointers_made=player_data['threePointersMade'],
            three_pointers_attempted=player_data['threePointersAttempted'],
            # Add more fields as needed
        )
        stats_instance.save()
# Make sure to adjust 'path_to_games.json' to the actual path of your games.json file and
#import your Stats model from your Django app.
#
# import json
# Load JSON Game data from the games.json file
with open('raw_data/games.json', 'r') as games_file:
    games_data = json.load(games_file)

# Iterate over the JSON data and create Shot model instances
# for game_item in games_data:
#     home_team_players = game_item['homeTeam']['players']
#     away_team_players = game_item['awayTeam']['players']
#
#     for player_data in home_team_players:
#         # Extract the shots data for the player
#         shots_data = player_data.get('shots', [])
#
#         # Iterate over the shots data and create Shot instances
#         for shot_data in shots_data:
#             # Create a Shot instance using the data from the JSON
#             shot_instance = Shot(
#                 player_id=player_data['id'],
#                 is_make=shot_data['isMake'],
#                 location_x=shot_data['locationX'],
#                 location_y=shot_data['locationY'],
#             )
#             shot_instance.save()

    # for player_data in away_team_players:
    #     # Extract the shots data for the player
    #     shots_data = player_data.get('shots', [])
    #
    #     # Iterate over the shots data and create Shot instances
    #     for shot_data in shots_data:
    #         # Create a Shot instance using the data from the JSON
    #         shot_instance = Shot(
    #             player_id=player_data['id'],
    #             is_make=shot_data['isMake'],
    #             location_x=shot_data['locationX'],
    #             location_y=shot_data['locationY'],
    #         )
    #         shot_instance.save()
# Make sure to adjust 'path_to_games.json' to the actual path of your games JSON file
# and import your Shot model from your Django app.
