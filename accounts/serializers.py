from rest_framework.serializers import ModelSerializer

from .models import (
    Employee, ManagerTeamEmployee, SalesTeamEmployee, SupportTeamEmployee)


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Employee
        exclude = [
            "password", "last_login", "is_active", "is_staff", "is_admin"
        ]
