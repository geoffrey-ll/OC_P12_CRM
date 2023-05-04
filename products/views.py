from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from CRM_EPIC_Events.settings import ADMIN_TEAM
from accounts.permissions import ContractPermission, EventPermission
from .models import Contract, Event
from .serializers import ContractSerializer, EventSerializer
from accounts.models import SalesTeamEmployee


class ContractViewSet(ModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermission]
    filterset_fields = ["closed"]
    search_fields = ["closed"]

    def get_queryset(self):
        user = self.request.user
        all = self.request.query_params.get("all")
        if all or user.team in ADMIN_TEAM:
            return Contract.objects.all()
        elif user.team == "SU":
            events_handle = Event.objects.filter(support_employee=user)
            return Contract.objects.filter(
                contract_number__in=[
                    event.contract.contract_number for event in events_handle])
        else:
            return Contract.objects.filter(
                client__id_sales_employee=self.request.user)

    # def perform_create(self, serializer):
    #     pass
    #
    # def perform_update(self, serializer):
    #     pass
    #
    # def perform_destroy(self, instance):
    #     pass


class EventViewSet(ModelViewSet):

    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventPermission]

    def get_queryset(self):
        user = self.request.user
        all = self.request.query_params.get("all")
        if all or user.team in ADMIN_TEAM:
            return Event.objects.all()
        elif user.team == "SU":
            return Event.objects.filter(support_employee=user)
        elif user.team == "SA":
            return Event.objects.filter(
                contract__client__id_sales_employee=user)

