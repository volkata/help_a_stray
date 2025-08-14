from django.db import models

from cat.models import Color
from cat.choices import CAT_GENDER_CHOICES


# Create your models here.
class CatSighting(models.Model):
    cat = models.ForeignKey('cat.Cat', on_delete=models.CASCADE, related_name='cat_sighting')
    district = models.ForeignKey('district.District', on_delete=models.CASCADE, related_name='cat_sighting')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='cat_sighting')
    color = models.ManyToManyField(Color, related_name='cat_sighting')
    gender = models.CharField(max_length=7, choices=CAT_GENDER_CHOICES)
    gave_food = models.BooleanField(default=False)
    gave_water = models.BooleanField(default=False)
    health_notes = models.TextField(blank=True, null=True)
    time_met = models.DateTimeField(auto_now_add=True)

