from django.urls import path

from .views import (
    NewsListCreateView,
    NewsView,
)

urlpatterns = [
    path('', NewsListCreateView.as_view()),
    path('<int:pk>/', NewsView.as_view()),
]
