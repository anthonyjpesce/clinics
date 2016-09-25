from clinics.models import Clinic
from rest_framework import serializers


class ClinicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Clinic

    def to_representation(self, instance):
        return instance.as_dict()