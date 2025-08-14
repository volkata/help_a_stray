from  django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import Profile

UserModel = get_user_model()

class AppUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'main_district', 'email']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'main_district']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'profile_photo']

class ProfileDeleteForm(AppUserCreationForm):
    ...