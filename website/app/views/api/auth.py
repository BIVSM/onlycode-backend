from app.views.api import APIView, APIError, takes_json
from app.models.token import Token
from app.forms import NewUserForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.db.utils import IntegrityError


def user_to_dict(user: User) -> dict:
    return {"username": user.username, "email": user.email}


class RegisterView(APIView):
    @takes_json
    def post(self, request: HttpRequest):
        form = NewUserForm(self.json_input)

        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError:
                raise APIError("User data should be unique", 409)

            return self.render_json(201, {"profile": user_to_dict(user)})
        else:
            raise APIError(form.errors.as_text(), 400)


class LoginView(APIView):
    @takes_json
    def post(self, request: HttpRequest):
        form = AuthenticationForm(self.json_input)
        if form.is_valid():
            user = form.get_user()
            token = Token.objects.create_token(user)
            return self.render_json(200, {"token": token.token})
        else:
            raise APIError(form.errors.as_text(), 400)