from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .forms import *
from .models import Location
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def index(request):
    location_list = Location.objects.order_by('-address')[:]
    template = loader.get_template('locations/index.html')
    form = LocationForm()
    context = {
        'location_list': location_list,
        'form': form
    }

    if request.method == "POST":
        query = request.POST.__getitem__('name')
        return HttpResponseRedirect(reverse('locations:select', args=(query,)))

    return HttpResponse(template.render(context, request))


@login_required
def select(request, query):
    session = requests.Session()
    response = session.get(
        'https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q=' + query)
    if not response:
        messages.info(request, 'No search result!')
        return HttpResponseRedirect('/locations/')
    select_list = response.json()
    template = loader.get_template('locations/select.html')
    context = {
        'query': query,
        'select_list': select_list,
    }

    if request.method == "POST":
        choose = request.POST.get('choice', False)
        if (choose):
            selected_choice = select_list[int(choose)]
            new_location = Location(x=selected_choice['x'],
                                    y=selected_choice['y'],
                                    name=selected_choice['nameEN'],
                                    address=selected_choice['addressEN'])
            if Location.objects.filter(x=new_location.x, y=new_location.y).exists():
                context = {
                    'query': query,
                    'select_list': select_list,
                    'error_message': "This location is known to HotZone. Please select again!",
                }
                return HttpResponse(template.render(context, request))
            else:
                new_location.save()
                return redirect('/locations/')
        else:
            context = {
                'query': query,
                'select_list': select_list,
                'error_message': "You didn't select a choice. Please select again!",
            }
            return HttpResponse(template.render(context, request))
    return HttpResponse(template.render(context, request))
