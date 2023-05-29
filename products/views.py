"""Views de l'app products."""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Contract, Event
from .serializers import ContractSerializer, EventSerializer
from CRM_EPIC_Events.settings import ADMIN_TEAM
from accounts.permissions import ContractPermission, EventPermission


class ContractViewSet(ModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermission]
    filter_search_fields = [
        "client__first_name", "client__last_name", "client__email",
        "date_created", "amount"
    ]
    filterset_fields = filter_search_fields
    search_fields = filter_search_fields

    def get_queryset(self):
        user = self.request.user
        param_all = self.request.query_params.get("all")

        if param_all or user.team in ADMIN_TEAM:
            return Contract.objects.all()
        elif user.team == "SU":
            events_handle = Event.objects.filter(support_employee=user)
            return Contract.objects.filter(
                contract_number__in=[event.contract.contract_number
                                     for event in events_handle])
        else:
            return Contract.objects.filter(
                client__sales_employee=self.request.user)


class EventViewSet(ModelViewSet):

    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventPermission]
    filter_search_fields = [
        "contract__client__first_name", "contract__client__last_name",
        "contract__client__email", "start_event", "end_event"
    ]
    filterset_fields = filter_search_fields
    search_fields = filter_search_fields

    def get_queryset(self):
        user = self.request.user
        param_all = self.request.query_params.get("all")

        if param_all or user.team in ADMIN_TEAM:
            return Event.objects.all()
        elif user.team == "SU":
            return Event.objects.filter(support_employee=user)
        elif user.team == "SA":
            return Event.objects.filter(
                contract__client__sales_employee=user)
