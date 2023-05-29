"""Serializer de l'app persons."""
from rest_framework.serializers import ModelSerializer

from .models import Client, Prospect


class ClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"


class ProspectSerializer(ModelSerializer):

    class Meta:
        model = Prospect
        fields = "__all__"
