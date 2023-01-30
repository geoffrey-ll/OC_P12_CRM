from rest_framework.serializers import ModelSerializer

from .models import Employee


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Employee
        exclude = [
            "password", "last_login", "is_active", "is_staff", "is_admin"
        ]

    # def to_representation(self, instance):
    #     pass
