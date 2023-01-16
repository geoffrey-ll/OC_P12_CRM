from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from accounts.permissions import ContractPermission, EventPermission
from .models import Contract, Event
from .serializers import ContractSerializer, EventSerializer
from accounts.models import SalesTeamEmployee


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [ContractPermission]

    def get_queryset(self):
        all = self.request.query_params.get("all")
        if all:
            return Contract.objects.all()
        else:
            print(f"\n\nTEST\n{isinstance(self.request.user, SalesTeamEmployee)}")
            print(f"\n\nTest\n{self.request.user}\n")
            return Contract.objects.filter(
                client__id_sales_employee=self.request.user)


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [EventPermission]

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
