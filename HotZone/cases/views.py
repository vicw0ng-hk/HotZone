from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.
case = {}


def add(request):
    context = {'CaseForm': CaseForm(),
               'PatientForm': PatientForm(),
               'VirusForm': VirusForm()
               }
    if request.method == 'POST':
        tmp = request.POST
        case['case_no'] = tmp.__getitem__('case_no')
        case['date_confirmed'] = tmp.__getitem__('date_confirmed')
        case['local'] = tmp.__getitem__('local')
        case['patient_name'] = tmp.__getitem__('patient_name')
        case['patient_id'] = tmp.__getitem__('patient_id')
        case['patient_birthday'] = tmp.__getitem__('patient_birthday')
        case['virus'] = tmp.__getitem__('virus_name')
        new_patient = Patient(
            name=case['patient_name'], hkid=case['patient_id'], birthday=case['patient_birthday'])
        new_patient.save()
        new_case = Case(no=case['case_no'], date_confirmed=case['date_confirmed'], local=case['local'],
                        patient=new_patient, virus=Virus.objects.get(pk=int(case['virus'])))
        new_case.save()
        return redirect('/cases/caselocation?no='+case['case_no'])
    return render(request, 'cases/add.html', context)


def create_virus(request):
    form = NewVirusForm()
    context = {'form': form}
    if request.method == 'POST':
        tmp = request.POST
        new_virus = Virus(name=tmp.__getitem__('virus_name'), common_name=tmp.__getitem__('virus_name'),
                          max_inf_period=tmp.__getitem__('max_inf_period'))
        new_virus.save()
        return redirect('/cases')
    return render(request, 'cases/create_virus.html', context)


def main(request):
    cases = Case.objects.order_by('-no').reverse()
    for case in cases:
        case.local = case.local.replace('1', 'local').replace('2', 'imported')
    context = {'cases': cases}
    return render(request, 'cases/main.html', context)


def caselocation(request):
    case_num = request.GET.get('no')
    caseLocations = CaseLocation.objects.filter(case__no=case_num)
    for caselocation in caseLocations:
        caselocation.category = caselocation.category.replace(
            '1', 'Residence').replace('2', 'Workplace').replace('3', 'Visit')
    context = {'caseLocations': caseLocations, 'no': case_num}
    return render(request, 'cases/caselocation.html', context)


def caselocation_add(request):
    case_num = request.GET.get('no')
    case = Case.objects.filter(no=case_num).first()
    form = CaseLocationForm()
    if request.method == 'POST':
        tmp = request.POST
        loc = tmp.__getitem__('location')
        dt_f = tmp.__getitem__('date_from')
        dt_t = tmp.__getitem__('date_to')
        cat = tmp.__getitem__('category')
        new_caseLocation = CaseLocation(location=Location.objects.get(pk=loc),
                                        date_from=dt_f, date_to=dt_t, category=cat,
                                        case=case)
        new_caseLocation.save()
        return redirect('/cases/caselocation?no=' + case_num)
    context = {'form': form, 'no': case_num}
    return render(request, 'cases/case_add_location.html', context)
