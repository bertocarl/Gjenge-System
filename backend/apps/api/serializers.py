from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField

from apps.api.models import Transportation, Checkpoint
from apps.catalog.models import HazardousMaterial


class CheckpointSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = Checkpoint
        fields = ('id', 'location', 'created_at', 'data')


class HazardousMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = HazardousMaterial
        fields = ('kind', 'repercussion')


class TransportationSerializer(serializers.ModelSerializer):
    start_point = PointField()
    end_point = PointField()
    type_of_hazardous_material = HazardousMaterialSerializer()

    class Meta:
        model = Transportation

        fields = (
            'id', 'start_point', 'end_point', 'checkpoint_set', 'volume', 'distance', 'risk_value',
            'type_of_hazardous_material'
        )
