from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages


# Create your views here.
case = {}
def add(request):
    form = CaseForm()
    context = {'form': form}
    if request.method == 'POST':
        tmp = request.POST
        case['case_no'] = tmp.__getitem__('case_no')
        case['date_confirmed'] = tmp.__getitem__('date_confirmed')
        case['local'] = tmp.__getitem__('local')
        return redirect('/cases/add/patient')
    return render(request, 'cases/add.html', context)


def add_patient(request):
    form = PatientForm()
    context = {'form': form}
    if request.method == 'POST':
        tmp = request.POST
        case['patient_name'] = tmp.__getitem__('patient_name')
        case['patient_id'] = tmp.__getitem__('patient_id')
        case['patient_birthday'] = tmp.__getitem__('patient_birthday')
        return redirect('/cases/add/virus')
    return render(request, 'cases/add_patient.html', context)


def add_virus(request):
    form = VirusForm()
    context = {'form': form}
    if request.method == 'POST':
        tmp = request.POST
        case['virus'] = tmp.__getitem__('virus_name')
        return redirect('/cases/add/location')
    return render(request, 'cases/add_virus.html', context)
    

def add_location(request):
    form = CaseLocationForm()
    context = {'form': form}
    if request.method == 'POST':
        print(case)
        tmp = request.POST
        case['location'] = tmp.__getitem__('location')
        case['date_from'] = tmp.__getitem__('date_from')
        case['date_to'] = tmp.__getitem__('date_to')
        case['category'] = tmp.__getitem__('category')
        new_patient = Patient(name=case['patient_name'], hkid=case['patient_id'], birthday=case['patient_birthday'])
        new_patient.save()
        new_case = Case(no=case['case_no'], date_confirmed=case['date_confirmed'], local=case['local'], patient=new_patient, virus=Virus.objects.get(pk=int(case['virus'])))
        new_case.save()
        new_caseLocation = CaseLocation(location=Location.objects.get(pk=int(case['location'])), date_from=case['date_from'], date_to=case['date_to'], category=case['category'], case=new_case)
        new_caseLocation.save()
        messages.warning(request, 'Success!')
        return redirect('/cases/add')
    return render(request, 'cases/add_location.html', context)

def create_virus(request):
    form = NewVirusForm()
    context = {'form': form}
    if request.method == 'POST':
        tmp = request.POST
        new_virus = Virus(name=tmp.__getitem__('virus_name'), common_name=tmp.__getitem__('virus_name'), max_inf_period=tmp.__getitem__('max_inf_period')) 
        new_virus.save()
        return redirect('/cases/add/virus')
    return render(request, 'cases/create_virus.html', context)
