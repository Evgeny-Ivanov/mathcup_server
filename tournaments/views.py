from rest_framework import generics, filters
from rounds.models import Round
from rounds.serializers import RoundSerializer
from common.permissions import IsAdminUserOrReadOnly
from .models import Tournament
from .serializers import TournamentSerializer
from .permissions import IsTournamentPublished


class TournamentListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = TournamentSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('create_date',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Tournament.objects.all()

        return Tournament.objects.published()


class TournamentView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdminUserOrReadOnly, IsTournamentPublished)
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer


class TournamentRoundListView(generics.ListAPIView):
    serializer_class = RoundSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('start', 'end')
    pagination_class = None

    def get_queryset(self):
        queryset = Round.objects.published()
        if self.request.user.is_staff:
            queryset = Round.objects.all()

        tournament_pk = self.kwargs['pk']
        return queryset.filter(tournament_id=tournament_pk)

