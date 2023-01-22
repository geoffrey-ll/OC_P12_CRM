from rest_framework.serializers import ModelSerializer

from .models import Company, Location


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"

    # def to_representation(self, instance):
    #     pass


class LocationSerializer(ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"

    # def to_representation(self, instance):
    #     pass
