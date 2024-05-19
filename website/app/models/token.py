import uuid
import jwt

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings


class TokenManager(models.Manager):
    def create_token(self, user: User):
        encoded = jwt.encode({"username": user.username, "uuid": str(uuid.uuid4())}, user.password, algorithm="HS256")
        token = self.model(user=user, token=encoded)
        token.save()
        return token


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    objects = TokenManager()

    def __str__(self):
        return self.token

    @property
    def is_valid(self) -> bool:
        return (timezone.now() - self.date_created).seconds < settings.TOKEN_SESSION_LIFETIME * 60 * 60 and self.check_token()

    def check_token(self):
        try:
            return jwt.decode(self.token, self.user.password, algorithms=["HS256"])['username'] == self.user.username
        except jwt.exceptions.DecodeError:
            return False
