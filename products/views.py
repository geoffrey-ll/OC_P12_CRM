from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Contract, Event
from .serializers import ContractSerializer, EventSerializer


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer

    def get_queryset(self):
        return Contract.objects.all()


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.all()
