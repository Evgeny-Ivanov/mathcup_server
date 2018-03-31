from django.urls import path

from .views import (
    UserAnswerCreateOrUpdateView,
)

urlpatterns = [
    path('', UserAnswerCreateOrUpdateView.as_view()),
]
