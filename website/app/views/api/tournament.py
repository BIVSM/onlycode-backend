from app.views.api import APIView, APIError, takes_json
from app.models import Tournament

from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpRequest
from django.db import transaction
import ast


class TournamentView(APIView):
    @takes_json
    def get(self, request: HttpRequest):
        ...  # Get tournament by id

    @takes_json
    def post(self, request: HttpRequest):
        ...  # Change tournament by id


class TournamentCreateView(APIView):
    @takes_json
    def post(self, request: HttpRequest):
        tournament_model = Tournament.objects.create()
        return self.render_json(200, {'result': 'Tournament was successfully created', 'id': tournament_model.id})


class TournamentStartView(APIView):
    @takes_json
    def post(self, request: HttpRequest):
        tournament_id = self.json_input.get("id")
        if not tournament_id.isdigit():
            raise APIError("Tournament ID should be an integer", 422)
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            raise APIError("Tournament not found", 404)
        tournament.start_tournament()
        return self.render_json(204, {'result': f'Tournament with ID {tournament_id} started'})


class TournamentGetGameView(APIView):
    @takes_json
    def get(self, request: HttpRequest):
        ...  # Get game from tournament with id = ...


class TournamentUploadSolutionView(APIView):
    @takes_json
    def get(self, request: HttpRequest):
        ...  # Add solution to the tournament with id = ... from user request.user


class TournamentRegisterView(APIView):
    @takes_json
    def post(self, request: HttpRequest):
        tournament_id = self.json_input.get("tournament_id")
        user_id = self.json_input.get("user_id")
        if not tournament_id.isdigit():
            raise APIError("Tournament ID should be an integer", 422)
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            raise APIError("Tournament not found", 404)
        try:
            is_player_exists = tournament.players.get(pk=user_id)
        except:
            is_player_exists = None

        if is_player_exists is None and len(tournament.players.all()) < tournament.max_of_players:
            current_user = User.objects.get(pk=user_id)
            tournament.players.add(current_user)
            return self.render_json(200, {'status': 'done'})
        elif is_player_exists is None:
            return self.render_json(200, {'status': 'registration limit'})
        else:
            return self.render_json(200, {'status': 'already registered'})
