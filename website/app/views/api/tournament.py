from app.views.api import APIView, APIError, takes_json
from app.models import Tournament

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
    def post(self, request: HttpRequest):
        ...  # Create empty tournament, return id


class TournamentStartView(APIView):
    def post(self, request: HttpRequest):
        ...  # Start tournament with id = ...


class TournamentGetGameView(APIView):
    def get(self, request: HttpRequest):
        ...  # Get game from tournament with id = ...


class TournamentUploadSolutionView(APIView):
    def get(self, request: HttpRequest):
        ...  # Add solution to the tournament with id = ... from user request.user


class TournamentRegisterView(APIView):
    def post(self, request: HttpRequest):
        ...  # Register on tournament with user from request.user
