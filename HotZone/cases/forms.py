from django import forms
from django.forms import ModelForm
import datetime
from .models import *
from HotZone_config import settings


class caseForm(forms.ModelForm):
    case_no = forms.CharField(widget=forms.TextInput())
    date_confirmed = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), localize=True)
    local = forms.CharField(widget=forms.Select(choices=[('1', 'local'), ('2', 'imported')]))

    patient_name = forms.CharField(widget=forms.TextInput())
    patient_id = forms.CharField(widget=forms.TextInput())
    patient_birthday = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), localize=True)

    virus_name = forms.CharField(widget=forms.TextInput())
    virus_common_name = forms.CharField(widget=forms.TextInput())
    max_inf_period = forms.CharField(widget=forms.TextInput())

    location = forms.ModelChoiceField(queryset=Location.objects.all())
    date_from = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), localize=True)
    date_to = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), localize=True)
    category = forms.CharField(widget=forms.Select(choices=[('1', 'Residence'), ('2', 'Workplace'), ('3', 'Visit')]))

    class Meta:
        model = Case
        fields = '__all__'