from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .managers import EventManager
from .models import Contract, Event
from CRM_EPIC_Events.commons_functions import datetime_to_representation


class ContractSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = "__all__"

    # def to_representation(self, instance):
    #     pass


class EventSerializer(ModelSerializer):
    # support_employee = SerializerMethodField("get_support_employee")
    # contract = SerializerMethodField("get_contract")

    class Meta:
        model = Event
        fields = "__all__"

    # def get_support_employee(self, instance):
    #     return instance.support_employee.__str__()
    #
    # def get_contract(self, instance):
    #     return instance.contract.__str__()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["support_employee"] = instance.support_employee.__str__()
        ret["contract"] = instance.contract.__str__()
        datetime_fields = [
            ("start_event", instance.start_event),
            ("end_event", instance.end_event),
            ("date_created", instance.date_created),
            ("date_updated", instance.date_updated)
        ]
        for datetime_field in datetime_fields:
            ret[datetime_field[0]] = datetime_to_representation(datetime_field[1])
        return ret
    #
    # def create(self, validated_data):
    #     print(validated_data)
    #     em = EventManager()
    #     em.model = Event
    #     return em.create(**validated_data)
    #
