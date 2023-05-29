"""Serializer de l'app products."""
from rest_framework.serializers import ModelSerializer

from .models import Contract, Event
# from CRM_EPIC_Events.commons_functions import datetime_to_str


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
        # todo -> DATETIME_FORMAT est plus lisible, mais il ne prend pas
        #  le fuseau horaire malgré le tz.
        # datetime_fields = [
        #     ("start_event", instance.start_event),
        #     ("end_event", instance.end_event),
        #     ("date_created", instance.date_created),
        #     ("date_updated", instance.date_updated)
        # ]
        # for datetime_field in datetime_fields:
        #     ret[datetime_field[0]] = datetime_to_str(datetime_field[1])
        return ret
