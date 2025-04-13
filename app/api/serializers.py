from rest_framework import serializers
from park.models import Park


class ParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Park
        fields = [
            "name",
            "description",
            "category",
            "status",
            "full_address",
            "street",
            "lat",
            "lon",
        ]
