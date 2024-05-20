from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views.api.auth import RegisterView, LoginView, ProfileView
from .views.api.game import GameView, GameCreateView
from .views.api.compile import CompileView
from .views.api.tournament import TournamentRegisterView, TournamentUploadSolutionView
from .views.api.tournament import TournamentGetGameView, TournamentCreateView
from .views.api.tournament import TournamentView, TournamentStartView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("games/", GameView.as_view(), name="games"),
    path("games/create/", GameCreateView.as_view(), name="create_game"),
    path("compile/", CompileView.as_view(), name="compile"),
    path("tournaments/", TournamentView.as_view(), name="tournaments"),
    path("tournaments/start/", TournamentStartView.as_view(), name="start_tournament"),
    path("tournaments/upload/", TournamentUploadSolutionView.as_view(), name="tournament_upload"),
    path("tournaments/game/", TournamentGetGameView.as_view(), name="tournament_game"),
    path("tournaments/create/", TournamentCreateView.as_view(), name="create_tournament"),
    path("tournaments/register/", TournamentRegisterView.as_view(), name="tournament_register")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
