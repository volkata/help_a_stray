from cloudinary.models import CloudinaryField
from django.db import models

# Create your models here.
class District(models.Model):
    name = models.CharField(max_length=40)
    photo = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name