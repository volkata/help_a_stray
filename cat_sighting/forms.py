from django import forms

from cat.models import Cat
from cat_sighting.models import CatSighting
from district.models import District


class CatSightingPartOneForm(forms.ModelForm):
    class Meta:
        model= CatSighting
        fields = ['district', 'color', 'gender']
        widgets = {   'color': forms.SelectMultiple(attrs={'class': 'color-select', 'size': '5'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.all()
        self.fields['district'].initial = user.main_district

class CatSightingExistingForm(forms.ModelForm):
    class Meta:
        model = CatSighting
        fields = ['gave_food','gave_water','health_notes']

class CatSightingNewForm(forms.ModelForm):
    gave_food = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    gave_water = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    class Meta:
        model = Cat
        fields = ['name', 'photo', 'age','gave_food', 'gave_water', 'health_notes']