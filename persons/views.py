from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Client, Prospect
from .serializers import ClientSerializer, ProspectSerializer
from accounts.permissions import PersonPermission
from CRM_EPIC_Events.settings import ADMIN_TEAM


# Create your views here.
class PersonViewSet(ModelViewSet):

    # serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, PersonPermission]

    def get_serializer_class(self):
        pass

    def get_queryset(self):
        user = self.request.user
        all = self.request.query_params.get("all")
        if all or user.team in ADMIN_TEAM:
            clients = Client.objects.all()
            prospects = Prospect.objects.all()
            return clients, prospects

    def perform_create(self, serializer):
        pass

    def perform_update(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass
