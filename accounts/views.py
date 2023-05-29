"""Views pour les employees."""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from CRM_EPIC_Events.commons_functions import \
    (get_supports_of_clients_handle, get_sales_of_events_handle)
from CRM_EPIC_Events.settings import ADMIN_TEAM, EMPLOYEE_TEAM
from .models import Employee
from .permissions import AccountPermission
from .serializers import AccountSerializer


class AccountViewSet(ModelViewSet):
    """Views des employees."""

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, AccountPermission]

    def get_queryset(self):
        user = self.request.user
        param_all = self.request.query_params.get("all")
        param_MA = self.request.query_params.get("manager")
        param_SA = self.request.query_params.get("sale")
        param_SU = self.request.query_params.get("support")

        if param_MA or param_SA or param_SU:
            team_filters = []
            if param_MA:
                team_filters.append("MA")
            if param_SA:
                team_filters.append("SA")
            if param_SU:
                team_filters.append("SU")
            return Employee.objects.filter(
                team__in=[team for team in team_filters])

        else:
            if param_all or user.team in ADMIN_TEAM:
                return Employee.objects.filter(team__in=EMPLOYEE_TEAM)
            else:
                user_instance = Employee.objects.filter(id=user.id)
                if user.team == "SA":
                    support_of_clients_handle = \
                        get_supports_of_clients_handle(user)
                    return support_of_clients_handle | user_instance
                elif user.team == "SU":
                    sales_of_events_handle = get_sales_of_events_handle(user)
                    return sales_of_events_handle | user_instance
