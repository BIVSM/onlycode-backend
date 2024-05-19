from app.views.api import APIView, APIError, takes_json
from app.models import Game

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpRequest
import ast


def user_to_dict(user: User) -> dict:
    return {"username": user.username, "email": user.email}


class GameView(APIView):
    @takes_json
    def get(self, request: HttpRequest):
        game_id = str(self.json_input.get("id"))
        if not game_id.isdigit():
            raise APIError("Game ID should be an integer", 422)
        else:
            try:
                game = Game.objects.get(pk=game_id)
            except:
                raise APIError("Requested game not found", 404)
            serialized_game = serializers.serialize('json', [game])
            serialized_game = ast.literal_eval(serialized_game)[0]
            serialized_game['fields']['id'] = serialized_game['pk']
            serialized_game = serialized_game['fields']
            try:
                with open(f'media/{serialized_game["rules"]}', 'r') as file:
                    serialized_game['rules'] = file.read()
            except:
                serialized_game['rules'] = 'Rules does not exist'
            return self.render_json(200, {'game': serialized_game})


class GameCreateView(APIView):
    @takes_json
    def post(self, request: HttpRequest):
        ...  # TODO
