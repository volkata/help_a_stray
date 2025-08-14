from django import forms
from actions.models import Action

class ActionEditForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['treatment_cost', 'priority']