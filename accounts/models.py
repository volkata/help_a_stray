from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

from accounts.managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[MinLengthValidator(3)],
        error_messages={'unique': 'A user with that username already exists.'}
    )
    main_district = models.ForeignKey('district.District', on_delete=models.CASCADE, related_name='users')
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def is_district_admin(self):
        return self.groups.filter(name='district admin').exists()

    def is_vet(self):
        return self.groups.filter(name='Vet').exists()

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    cats_interacted = models.ManyToManyField('cat.Cat', related_name='users', blank=True)
    profile_photo = CloudinaryField('image', null=True, blank=True)
    karma_points = models.IntegerField(default=0)

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()