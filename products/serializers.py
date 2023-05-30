"""Serializer de l'app products."""
from rest_framework.serializers import ModelSerializer

from .models import Contract, Event


class ContractSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = "__all__"


class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["support_employee"] = instance.support_employee.__str__()
        ret["contract"] = instance.contract.__str__()
        return ret
