from rest_framework import serializers

from cat.models import Cat


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ['id', 'name', 'age', 'neutered', 'chipped', 'health_notes']