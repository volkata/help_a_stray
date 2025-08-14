from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible




@deconstructible
class UniqueCatInDistrict:
    def __init__(self, message=None):
        self.message = message or 'A cat with this name exists in this district!'

    def __call__(self, instance):
        from cat.models import Cat
        exists = Cat.objects.filter(
            name=instance.name,
            district=instance.district,
        ).exclude(pk=instance.pk).exists()
        if exists:
            raise ValidationError({'name': self.message})
