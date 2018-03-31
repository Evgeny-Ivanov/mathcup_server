from rest_framework.permissions import BasePermission
from tasks.models import Task


class IsRoundRunning(BasePermission):
    def has_permission(self, request, view):
        task_id = request.data.get('task', None)
        task = Task.objects.get(id=task_id)
        return task.round.is_running()
