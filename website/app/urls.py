from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views.api.auth import RegisterView, LoginView, ProfileView
from .views.api.game import GameView, GameCreateView
from .views.api.compile import CompileView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("games/", GameView.as_view(), name="games"),
    path("games/create/", GameCreateView.as_view(), name="create_game"),
    path("compile/", CompileView.as_view(), name="compile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
