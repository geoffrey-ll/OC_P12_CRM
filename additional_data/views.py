"""Views de l'app additional_data."""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Company, Location
from .serializers import CompanySerializer, LocationSerializer
from CRM_EPIC_Events.commons_functions import (
    get_clients_handle, get_events_handle,
    get_locations_of_clients_and_of_events)
from CRM_EPIC_Events.settings import ADMIN_TEAM
from accounts.permissions import CompanyPermission, LocationPermission


class CompanyViewSet(ModelViewSet):

    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, CompanyPermission]

    def get_queryset(self):
        user = self.request.user
        param_all = self.request.query_params.get("all")

        if param_all or user.team in ADMIN_TEAM:
            return Company.objects.all()
        elif user.team == "SA":
            clients_handle = get_clients_handle(user)
            return Company.objects.filter(
                id__in=[client.company.id for client in clients_handle])
        elif user.team == "SU":
            events_handle = get_events_handle(user)
            return Company.objects.filter(
                id__in=[event.contract.client.company.id
                        for event in events_handle])


class LocationViewSet(ModelViewSet):

    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, LocationPermission]

    def get_queryset(self):
        user = self.request.user
        param_all = self.request.query_params.get("all")

        if param_all or user.team in ADMIN_TEAM:
            return Location.objects.all()
        elif user.team == "SA" or user.team == "SU":
            return get_locations_of_clients_and_of_events(user)
