from django.db import models

# Create your models here.
class District(models.Model):
    name = models.CharField(max_length=40)
    photo = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name