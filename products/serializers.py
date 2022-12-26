from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Contract, Event


class ContractSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = "__all__"


class EventSerializer(ModelSerializer):
    support_employee = SerializerMethodField("get_support_employee")
    contract = SerializerMethodField("get_contract")

    class Meta:
        model = Event
        fields = "__all__"

    def get_support_employee(self, instance):
        return instance.support_employee.__str__()

    def get_contract(self, instance):
        return instance.contract.__str__()

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     return ret
