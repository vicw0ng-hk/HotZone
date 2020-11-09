from django import forms
from django.forms import ModelForm

from .models import Location


class LocationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Input location...'}))

    class Meta:
        model = Location
        fields = '__all__'
