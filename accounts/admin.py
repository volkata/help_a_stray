from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.models import Profile

UserModel = get_user_model()
# Register your models here.
@admin.register(UserModel)
class ModelNameAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields":('main_district',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields":('main_district',)}),
    )
    list_display = UserAdmin.list_display + ('main_district',)
    list_filter = UserAdmin.list_filter + ('main_district',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...