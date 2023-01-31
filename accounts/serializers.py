from rest_framework.serializers import ModelSerializer

from .models import (
    Employee, ManagerTeamEmployee, SalesTeamEmployee, SupportTeamEmployee)


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Employee
        exclude = [
            "password", "last_login", "is_active", "is_staff", "is_admin"
        ]

    # def create(self, validated_data):
    #     print(f"\nvalidated_data\n{validated_data}\n")
    #     if validated_data["team"] == "SA":
    #         ModelClass = SalesTeamEmployee
    #     elif validated_data["team"] == "SU":
    #         ModelClass = SupportTeamEmployee
    #     elif validated_data["team"] == "MA":
    #         ModelClass = ManagerTeamEmployee
    #
    #     instance = ModelClass._default_manager.create(**validated_data)
    #     return instance
    #
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     if ret["password"]:
    #         ret["password"] = "********"
    #     return ret
