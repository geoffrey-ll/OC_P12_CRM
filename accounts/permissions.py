from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS

from products.models import Contract, Event


class EventPermissions(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticated(detail="Dois être login.")
        return True


    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            raise NotAuthenticated(detail="Dois être login.")
        user = request.user
        user_team = user.team
        if user_team == "WM":
            return True
        else:
            pk_event = view.kwargs.get("pk")
            event = Event.objects.get(id=pk_event)
            if user_team == "SU":
                print(f"\n\nTEST\n{event.support_employee.id == user.id}\n")
                return event.support_employee.id == user.id
            if user_team == "SA":
                return event.contract.client.id_sales_employee.id == user.id

        return False
