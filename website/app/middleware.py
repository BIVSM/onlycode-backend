from app.models.token import Token
import re

from django.http import HttpRequest
from django.contrib.auth import login


def token_auth_middleware(get_response):
    def middleware(request: HttpRequest):
        match_user_token = re.match(r'^Bearer (.+)$', request.headers.get("Authorization", ""))
        if match_user_token:
            token = Token.objects.filter(token=match_user_token.group(1)).first()
            if token and token.is_valid:
                login(request, token.user)

        response = get_response(request)

        return response

    return middleware
