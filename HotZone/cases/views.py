from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import numpy as np
from .cluster import Cluster
import datetime

# Create your views here.
case = {}


@login_required
def add(request):
    context = {'CaseForm': CaseForm(), 'PatientForm': PatientForm(), 'VirusForm': VirusForm()}
    if request.method == 'POST':
        tmp = request.POST
        case['case_no'] = tmp.__getitem__('case_no')
        if not case['case_no'].isdigit():
            messages.info(request, 'Case number must be an integer!')
            return HttpResponseRedirect('/cases/add')
        if Case.objects.filter(no=case['case_no']).exists():
            messages.info(request, 'Case exists!')
            return HttpResponseRedirect('/cases/add')
        case['date_confirmed'] = tmp.__getitem__('date_confirmed')
        case['local'] = tmp.__getitem__('local')
        case['patient_name'] = tmp.__getitem__('patient_name')
        case['patient_id'] = tmp.__getitem__('patient_id')
        case['patient_birthday'] = tmp.__getitem__('patient_birthday')
        case['virus'] = tmp.__getitem__('virus_name')
        new_patient = Patient(name=case['patient_name'], hkid=case['patient_id'],
                              birthday=case['patient_birthday'])
        new_patient.save()
        new_case = Case(no=case['case_no'], date_confirmed=case['date_confirmed'], local=case['local'],
                        patient=new_patient, virus=Virus.objects.get(pk=int(case['virus'])))
        new_case.save()
        return redirect('/cases/caselocation?no='+case['case_no'])
    return render(request, 'cases/add.html', context)


@login_required
def create_virus(request):
    form = NewVirusForm()
    context = {'form': form}
    if request.method == 'POST':
        tmp = request.POST
        if not tmp.__getitem__('max_inf_period').isdigit():
            messages.info(request, 'Maximum infectious period must be an integer!')
            return HttpResponseRedirect('/cases/add/create_virus')
        new_virus = Virus(name=tmp.__getitem__('virus_name'),
                          common_name=tmp.__getitem__('virus_common_name'),
                          max_inf_period=tmp.__getitem__('max_inf_period'))
        new_virus.save()
        return redirect('/cases')
    return render(request, 'cases/create_virus.html', context)


@login_required
def main(request):
    cases = Case.objects.order_by('-no')[:]
    for case in cases:
        case.local = case.local.replace('1', 'Local').replace('2', 'Imported')
    context = {'cases': cases}
    return render(request, 'cases/main.html', context)


@login_required
def caselocation(request):
    case_num = request.GET.get('no')
    caseLocations = CaseLocation.objects.filter(case__no=case_num)
    for caselocation in caseLocations:
        caselocation.category = caselocation.category.replace('1', 'Residence').replace('2', 'Workplace').replace('3', 'Visit')
    context = {'caseLocations': caseLocations, 'no': case_num}
    return render(request, 'cases/caselocation.html', context)


@login_required
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
        new_caseLocation = CaseLocation(location=Location.objects.get(pk=loc),date_from=dt_f, 
                                        date_to=dt_t, category=cat,case=case)
        new_caseLocation.save()
        return redirect('/cases/caselocation?no=' + case_num)
    context = {'form': form, 'no': case_num}
    return render(request, 'cases/case_add_location.html', context)


@login_required
def cluster(request):
    form = VirusForm()
    if request.method == 'POST':
        tmp = request.POST
        _D = tmp.__getitem__('D')
        _T = tmp.__getitem__('T')
        _C = tmp.__getitem__('C')
        if not ((_D.isdigit() or not _D) and (_T.isdigit() or not _T) and (_C.isdigit() or not _C)):
            messages.info(request, 'D, T and C must be integers!')
            return HttpResponseRedirect('/cases/cluster')
        qs = CaseLocation.objects.filter(date_from=models.F('date_to'), case__virus__name__contains=Virus.objects.get(pk=tmp.__getitem__('virus_name'))).values_list('location__x', 'location__y', 'date_from', 'case__no')
        if len(qs) < 2:
            _messages = ['Not enough data!']
            context = {'messages': _messages}
            return render(request, 'cases/cluster_failed.html', context)
        D = int(_D) if _D else 200
        T = int(_T) if _T else 3
        C = int(_C) if _C else 2
        l = []
        for q in qs:
            tmp = []
            for i in range(4):
                tmp += [(q[i]-datetime.date(2020, 1, 1)).days] if i == 2 else [q[i]]
            l.append(tmp)
        v4 = np.array(l)
        data = Cluster(v4, D, T, C)
        overview, ans_list = Cluster.cluster(data)
        message = 'Performed clustering with D = {}, T = {} and C = {}'.format(D, T, C)
        context = {'overview': overview, 'ans': ans_list, 'D': D, 'T': T, 'C': C, 'form': form, 'message': message}
        return render(request, 'cases/cluster.html', context)
    context = {'form': form}
    return render(request, 'cases/cluster.html', context)
