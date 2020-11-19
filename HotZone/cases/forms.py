from django import forms
from .models import *


class CaseForm(forms.ModelForm):
    case_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_confirmed = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}), localize=True)
    local = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}, choices=[('1', 'Local'), ('2', 'Imported')]))

    class Meta:
        model = Case
        fields = '__all__'


class PatientForm(forms.ModelForm):
    patient_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    patient_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    patient_birthday = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}), localize=True)

    class Meta:
        model = Patient
        fields = '__all__'


class VirusForm(forms.ModelForm):
    virus_name = forms.ModelChoiceField(queryset=Virus.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Virus
        fields = ['name']


class CaseLocationForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    date_from = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}), localize=True)
    date_to = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}), localize=True)
    category = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}, choices=[('1', 'Residence'), ('2', 'Workplace'), ('3', 'Visit')]))

    class Meta:
        model = CaseLocation
        fields = '__all__'


class NewVirusForm(forms.ModelForm):
    virus_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    virus_common_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    max_inf_period = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Virus
        fields = '__all__'
