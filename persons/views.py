from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from collections import namedtuple

from .models import Client, Prospect
from .serializers import NotUserSerializer, ProspectSerializer, ClientSerializer
from accounts.permissions import PersonPermission
from CRM_EPIC_Events.settings import ADMIN_TEAM


AllClients = namedtuple("AllClients", ("clients", "prospects"))

# Create your views here.
class PersonViewSet(ModelViewSet):


    # serializer_class = NotUserSerializer
    permission_classes = [IsAuthenticated, PersonPermission]



    # def list(self, request, *args, **kwargs):
    #
    #     all_clients = AllClients(clients=Client.objects.all(),
    #                              prospects=Prospect.objects.all())
    #
    #     serializer = NotUserSerializer(all_clients)
    #     return Response(serializer.data)


    def get_serializer_class(self):
        if self.request.query_params.get("prospect"):
            return ProspectSerializer
        return ClientSerializer

    def get_queryset(self):
        user = self.request.user
        all = self.request.query_params.get("all")
        if self.request.query_params.get("prospect"):
            if all or user.team in ADMIN_TEAM:
                prospects = Prospect.objects.all()
            else:
                prospects = \
                    Prospect.objects.filter(last_sales_employee_contact=user)
            return prospects
        else:
            if all or user.team in ADMIN_TEAM:
                clients = Client.objects.all()
            else:
                clients = Client.objects.filter(sales_employee=user)
            return clients


    # def perform_create(self, serializer):
    #     pass
    #
    # def perform_update(self, serializer):
    #     pass
    #
    # def perform_destroy(self, instance):
    #     pass
