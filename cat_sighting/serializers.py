from rest_framework import serializers

from cat_sighting.models import CatSighting


class CatSightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatSighting
        fields = '__all__'