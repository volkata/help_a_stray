from django.contrib import admin
from django.utils.text import slugify
from cat.models import Cat



@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    pass