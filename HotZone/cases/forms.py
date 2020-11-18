from django import forms
from .models import *


class CaseForm(forms.ModelForm):
    case_no = forms.CharField(widget=forms.TextInput())
    date_confirmed = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), localize=True)
    local = forms.CharField(widget=forms.Select(choices=[('1', 'local'), ('2', 'imported')]))

    class Meta:
        model = Case
        fields = '__all__'


class PatientForm(forms.ModelForm):
    patient_name = forms.CharField(widget=forms.TextInput())
    patient_id = forms.CharField(widget=forms.TextInput())
    patient_birthday = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), localize=True)

    class Meta:
        model = Patient
        fields = '__all__'


class VirusForm(forms.ModelForm):
    virus_name = forms.ModelChoiceField(queryset=Virus.objects.all())

    class Meta:
        model = Virus
        fields = ['name']


class CaseLocationForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    date_from = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), localize=True)
    date_to = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), localize=True)
    category = forms.CharField(widget=forms.Select(choices=[('1', 'Residence'), ('2', 'Workplace'), ('3', 'Visit')]))

    class Meta:
        model = CaseLocation
        fields = '__all__'


class NewVirusForm(forms.ModelForm):
    virus_name = forms.CharField(widget=forms.TextInput())
    virus_common_name = forms.CharField(widget=forms.TextInput())
    max_inf_period = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Virus
        fields = '__all__'
