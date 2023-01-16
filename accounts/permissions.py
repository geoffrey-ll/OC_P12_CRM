from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS

from products.models import Contract, Event


def check_authenticated(request):
    if not request.user.is_authenticated:
        raise NotAuthenticated(detail="Dois être login.")


class ContractPermission(BasePermission):

    def has_permission(self, request, view):
        check_authenticated(request)
        return True

    def has_object_permission(self, request, view, obj):
        check_authenticated(request)

        user = request.user
        user_team = user.team
        if user_team == "WM":
            return True
        else:
            pk_contract = view.kwargs.get("pk")
            contract = Contract.objects.get(id=pk_contract)
            if user_team == "SA":
                return contract.client.id_sales_employee.id == user.id
            if user_team == "SU":
                return False


class EventPermission(BasePermission):

    def has_permission(self, request, view):
        check_authenticated(request)
        return True


    def has_object_permission(self, request, view, obj):
        check_authenticated(request)

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
