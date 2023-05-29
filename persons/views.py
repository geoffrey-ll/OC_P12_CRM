"""Views de l'app persons."""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Client, Prospect
from .serializers import ProspectSerializer, ClientSerializer
from accounts.permissions import PersonPermission
from CRM_EPIC_Events.commons_functions import (
    get_events_handle, get_clients_of_events_handle)
from CRM_EPIC_Events.settings import ADMIN_TEAM


class PersonViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, PersonPermission]
    filter_search_fields = ["first_name", "last_name", "email"]
    filterset_fields = filter_search_fields
    search_fields = filter_search_fields

    def get_serializer_class(self):
        """Choix du serializer.

        Client et Prospect partage le même endpoint.
        Par défaut, c'est Client qui est serializé.
        Pour sérializer Prospect, il faut : ?prospect=True dans l'URL.
        """
        if self.request.query_params.get("prospect"):
            return ProspectSerializer
        return ClientSerializer

    def get_queryset(self):
        user = self.request.user
        param_all = self.request.query_params.get("all")
        param_prospect = self.request.query_params.get("prospect")

        if param_prospect:
            if param_all or user.team in ADMIN_TEAM:
                prospects = Prospect.objects.all()
            else:
                prospects = Prospect.objects.filter(
                    sales_employee=user)
            return prospects

        else:
            if param_all or user.team in ADMIN_TEAM:
                clients = Client.objects.all()
            elif user.team == "SU":
                events_handle = get_events_handle(user)
                clients = get_clients_of_events_handle(events_handle)
            else:
                clients = Client.objects.filter(sales_employee=user)
            return clients
