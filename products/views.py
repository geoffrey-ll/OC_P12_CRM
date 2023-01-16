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
        user = self.request.user
        user_team = user.team
        return Event.objects.all()
        # if user_team == "MA" or user_team == "WM":
        #     return Event.objects.all()
        # else:
        #     if user_team == "SU":
        #         return Event.objects.filter(support_employee=user.id)
        #     elif user_team == "SA":
        #         return Event.objects.filter(
        #             contract__client__id_sales_employee=user.id)

    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)

        except Exception as e:
            raise ValidationError(str(e))
