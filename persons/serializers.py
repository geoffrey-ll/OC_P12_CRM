from rest_framework.serializers import ModelSerializer

from .models import Client, Prospect


class ClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"

    def to_representation(self, instance):
        pass


class ProspectSerializer(ModelSerializer):

    class Meta:
        model = Prospect
        fields = "__all__"

    def to_representation(self, instance):
        pass
