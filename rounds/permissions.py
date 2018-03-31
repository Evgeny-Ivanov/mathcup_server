from rest_framework.permissions import BasePermission, IsAdminUser
from .models import Round


class IsRoundRunning(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        round = Round.objects.get(id=pk)
        return round.is_running()


class IsRoundEnded(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        round = Round.objects.get(id=pk)
        return round.is_ended()


class IsRoundStarted(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        round = Round.objects.get(id=pk)
        return round.is_started()


class IsRoundPublished(IsAdminUser):
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        round = Round.objects.get(id=pk)
        is_admin = super().has_permission(request, view)
        return round.is_published or is_admin
