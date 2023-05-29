"""Serializers l'app accounts."""
from rest_framework.serializers import ModelSerializer

from .models import Employee


class AccountSerializer(ModelSerializer):
    """Serializer du model user."""

    class Meta:
        model = Employee
        exclude = [
            "password", "last_login", "is_staff"]
