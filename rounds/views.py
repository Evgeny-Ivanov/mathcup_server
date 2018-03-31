from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from common.permissions import IsAdminUserOrReadOnly
from tasks.models import Task
from answers.models import UserAnswer
from tasks.serializers import (
    TaskSerializer,
    TaskSerializerWithAnswer
)
from answers.serializers import (
    UserAnswerSerializer,
    UserAnswerWithCorrectSerializer
)
from .serializers import (
    RoundSerializer,
    RoundRatingSerializer,
    UserScoreSerializer,
)
from .permissions import (
    IsRoundEnded,
    IsRoundStarted,
    IsRoundPublished
)
from .models import Round
from .services import RoundSummarizeService
from .tasks import send_join_round_mail


class RoundCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Round.objects.all()
    serializer_class = RoundSerializer


class RoundView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsRoundPublished, IsAdminUserOrReadOnly)
    queryset = Round.objects.all()
    serializer_class = RoundSerializer


class RoundTasksListView(generics.ListAPIView):
    permission_classes = (IsRoundStarted,)
    pagination_class = None

    def get_serializer_class(self):
        round_pk = self.kwargs['pk']
        round = Round.objects.get(pk=round_pk)
        if round.is_ended():
            return TaskSerializerWithAnswer
        return TaskSerializer

    def get_queryset(self):
        round_pk = self.kwargs['pk']
        return Task.objects.filter(round_id=round_pk)


class RoundUsersView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        queryset = Round.objects.all()
        round = get_object_or_404(queryset, pk=pk)
        round.users.add(request.user)
        send_join_round_mail.delay(round.name, request.user.email)
        return Response()

    def delete(self, request, pk):
        queryset = Round.objects.all()
        round = get_object_or_404(queryset, pk=pk)
        round.users.remove(request.user)
        return Response()


class RoundRatingView(generics.ListAPIView):
    permission_classes = (IsRoundEnded,)
    serializer_class = RoundRatingSerializer
    pagination_class = None

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        round = Round.objects.get(id=pk)
        return RoundSummarizeService.get_round_rating(round)


class UserAnswerListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsRoundStarted)
    pagination_class = None

    def get_serializer_class(self):
        round_pk = self.kwargs['pk']
        round = Round.objects.get(pk=round_pk)
        if round.is_ended():
            return UserAnswerWithCorrectSerializer
        return UserAnswerSerializer

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get('pk')
        return UserAnswer.objects.filter(user=user, task__round=pk)


class UserScoreView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, IsRoundEnded)
    serializer_class = UserScoreSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        round = Round.objects.get(id=pk)
        user = self.request.user
        return RoundSummarizeService.get_user_score(round, user)
