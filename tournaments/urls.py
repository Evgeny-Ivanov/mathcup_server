from django.urls import path

from .views import (
    TournamentListCreateView,
    TournamentView,
    TournamentRoundListView,
)

urlpatterns = [
    path('', TournamentListCreateView.as_view()),
    path('<int:pk>/', TournamentView.as_view()),
    path('<int:pk>/rounds/', TournamentRoundListView.as_view()),
]
