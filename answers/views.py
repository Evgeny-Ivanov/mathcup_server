from rest_framework import generics, permissions
from .models import UserAnswer
from .serializers import UserAnswerSerializer
from .permissions import IsRoundRunning


class UserAnswerCreateOrUpdateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsRoundRunning)
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
