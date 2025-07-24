from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.text import slugify

import district
from cat.choices import CAT_GENDER_CHOICES, CAT_COLOR_CHOICES
from district.models import District


# Create your models here.

class Color(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Cat(models.Model):
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=7, choices = CAT_GENDER_CHOICES)
    color = models.ManyToManyField(Color, related_name='cats')
    slug = models.SlugField(max_length=30, unique=True)
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(38)])
    photo = models.URLField(null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='cats')
    locations_seen = models.CharField(max_length=100, blank=False, null=True)
    last_seen = models.DateTimeField(auto_now=True)
    last_fed = models.DateTimeField(),
    last_water = models.DateTimeField(),
    neutered = models.BooleanField(default=False)
    chipped = models.BooleanField(default=False)
    health_notes = {}

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.pk}")
            super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

# run in shell
# for code, name in CAT_COLOR_CHOICES:
#     Color.objects.get_or_create(code=code, defaults={'name': name})