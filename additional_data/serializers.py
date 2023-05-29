"""Serializer de l'app additional_data."""
from rest_framework.serializers import ModelSerializer

from .models import Company, Location


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class LocationSerializer(ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"
