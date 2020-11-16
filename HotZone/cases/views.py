from django.shortcuts import render
from django.http import HttpResponse
from .forms import *


# Create your views here.
def add(request):
    form = caseForm()
    context = {'form': form}
    return render(request, 'cases/add.html', context)
