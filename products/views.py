from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from accounts.permissions import EventPermissions
from .models import Contract, Event
from .serializers import ContractSerializer, EventSerializer


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer

    def get_queryset(self):
        return Contract.objects.all()


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [EventPermissions]

    def get_queryset(self):
        return Event.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)

        except Exception as e:
            raise ValidationError(str(e))
