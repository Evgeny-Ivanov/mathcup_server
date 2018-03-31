from rest_framework.permissions import IsAdminUser
from .models import Tournament


class IsTournamentPublished(IsAdminUser):
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        tournament = Tournament.objects.get(id=pk)
        is_admin = super().has_permission(request, view)
        return tournament.is_published or is_admin
