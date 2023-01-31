from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from CRM_EPIC_Events.commons_functions import \
    (get_supports_of_clients_handle, get_sales_of_events_handle)
from CRM_EPIC_Events.settings import ADMIN_TEAM, EMPLOYEE_TEAM
from .models import Employee
from .permissions import AccountPermission
from .serializers import AccountSerializer


class AccountViewSet(ModelViewSet):

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, AccountPermission]

    def get_queryset(self):
        user = self.request.user
        all = self.request.query_params.get("all")
        MA = self.request.query_params.get("manager")
        SA = self.request.query_params.get("sale")
        SU = self.request.query_params.get("support")

        if MA:
            return Employee.objects.filter(team="MA")
        elif SA:
            return Employee.objects.filter(team="SA")
        elif SU:
            return Employee.objects.filter(team="SU")
        else:
            if all or user.team in ADMIN_TEAM:
                return Employee.objects.filter(team__in=EMPLOYEE_TEAM)
            else:
                user_instance = Employee.objects.filter(id=user.id)
                if user.team == "SA":
                    support_of_clients_handle = get_supports_of_clients_handle(user)
                    return support_of_clients_handle | user_instance
                elif user.team == "SU":
                    sales_of_events_handle = get_sales_of_events_handle(user)
                    return sales_of_events_handle | user_instance

    # def perform_create(self, serializer):
    #     print(f"\nperform_create\n{self.__dict__}\n")
    #     team = Employee.PossibleTeam.SALES
    #     pass
    #
    # def perform_update(self, serializer):
    #     pass
    #
    # def perform_destroy(self, instance):
    #     pass
