from cloudinary.api import transformation
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator
from django.db import models

from cat.choices import CAT_GENDER_CHOICES
from cat.validators import UniqueCatInDistrict


# Create your models here.

class Color(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name



class Cat(models.Model):
    name = models.CharField(max_length=30) #validator for unique name in district in call method
    gender = models.CharField(max_length=7, choices = CAT_GENDER_CHOICES)
    color = models.ManyToManyField(Color, related_name='cats')
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(38)])
    photo = CloudinaryField('image', blank=True, null=True,
                            transformation={
                                'width':300,
                                'height':300,
                                'crop':'limit',
                                'quality':'auto'
                            })
    district = models.ForeignKey('district.District', on_delete=models.CASCADE, related_name='cats')
    last_seen = models.DateTimeField(auto_now=True)
    last_fed = models.DateTimeField(null=True, blank=True)
    last_water = models.DateTimeField(null=True, blank=True)
    neutered = models.BooleanField(default=False)
    chipped = models.BooleanField(default=False)
    health_notes = models.CharField(null=True, blank=True, max_length=500)
    approved = models.BooleanField(default=False)

    def last_fed_display(self):
        return self.last_fed.strftime("%Y-%m-%d %H:%M") if self.last_fed else "Never"

    def last_water_display(self):
        return self.last_water.strftime("%Y-%m-%d %H:%M") if self.last_water else "Never"

    def total_treatment_cost(self):
        return sum(a.treatment_cost for a in self.actions.all())

    def __str__(self) -> str:
        return self.name

    def clean(self):
        super().clean()
        UniqueCatInDistrict()(self)

    class Meta:
        permissions = [
            ('approve_cat', 'Can approve a cat'),
        ]


class HealthNotes(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='condition')
    condition = models.TextField(max_length=500)
    cost = models.PositiveIntegerField(default=0)
    def __str__(self) -> str:
        return self.condition

    class Meta:
        permissions = [
            ('set_treatment_cost', 'Can set treatment cost'),
        ]





# run in shell
# for code, name in CAT_COLOR_CHOICES:
#     Color.objects.get_or_create(code=code, defaults={'name': name})