from django.urls import path

from .views import (
    RoundCreateView,
    RoundView,
    RoundUsersView,
    RoundTasksListView,
    RoundRatingView,
    UserScoreView,
    UserAnswerListView,
)

urlpatterns = [
    path('', RoundCreateView.as_view()),
    path('<int:pk>/', RoundView.as_view()),
    path('<int:pk>/users/', RoundUsersView.as_view()),
    path('<int:pk>/tasks/', RoundTasksListView.as_view()),
    path('<int:pk>/rating/', RoundRatingView.as_view()),
    path('<int:pk>/users/current/score/', UserScoreView.as_view()),
    path('<int:pk>/answers/', UserAnswerListView.as_view()),
]
