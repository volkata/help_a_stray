from django.contrib import admin

from district.models import District


# Register your models here.
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass