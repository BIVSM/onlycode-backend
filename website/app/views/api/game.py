from app.views.api import APIView, APIError, takes_json
from app.models import Game

from django.core import serializers
from django.http import HttpRequest
from django.db import transaction
import ast


class GameView(APIView):
    @takes_json
    def get(self, request: HttpRequest):
        game_id = str(self.json_input.get("id"))
        if not game_id.isdigit():
            raise APIError("Game ID should be an integer", 422)
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            raise APIError("Requested game not found", 404)
        serialized_game = serializers.serialize('json', [game])
        serialized_game = ast.literal_eval(serialized_game)[0]
        serialized_game['fields']['id'] = serialized_game['pk']
        serialized_game = serialized_game['fields']
        try:
            with game.rules.open() as file:
                serialized_game['rules'] = file.read()
        except ValueError:
            serialized_game['rules'] = 'Rules does not exist'
        return self.render_json(200, {'game': serialized_game})

    @takes_json
    def post(self, request: HttpRequest):
        game_id = str(self.json_input.get("id"))
        with transaction.atomic():
            game_model = Game.objects.get(pk=game_id)
            if self.json_input.get("name"):
                game_model.name = str(self.json_input.get("name"))
            if self.json_input.get("number_of_players"):
                game_model.number_of_players = str(self.json_input.get("number_of_players"))
            if self.json_input.get("win_point"):
                game_model.win_point = str(self.json_input.get("win_point"))
            if self.json_input.get("lose_point"):
                game_model.lose_point = str(self.json_input.get("lose_point"))
            if request.FILES.get('ideal_solution') is not None:
                game_model.ideal_solution = request.FILES.get('ideal_solution')
            if request.FILES.get('play') is not None:
                game_model.play = request.FILES.get('play')
            if request.FILES.get('visualiser') is not None:
                game_model.visualiser = request.FILES.get('visualiser')
            if request.FILES.get('rules') is not None:
                game_model.rules = request.FILES.get('rules')
            game_model.save()
        return self.render_json(204, {'result': 'Game ' + game_id + ' changed'})


class GameCreateView(APIView):
    def post(self, request: HttpRequest):
        game_model = Game.objects.create()
        return self.render_json(200, {'result': 'Game was successfully created', 'id': game_model.id})
