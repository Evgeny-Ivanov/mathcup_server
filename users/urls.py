from django.urls import path

from users.views import (
    sign_up_step1,
    sign_up_step2,
    sign_in,
    logout_view,
    RetrieveUpdateView,
)

urlpatterns = [
    path('signup/step1/', sign_up_step1),
    path('signup/step2/', sign_up_step2),
    path('signin/', sign_in),
    path('logout/', logout_view),
    path('current/', RetrieveUpdateView.as_view()),
]