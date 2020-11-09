from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .forms import *
from .models import Location
import requests
# Create your views here.


def index(request):
    location_list = Location.objects.order_by('-addressZH')[:]
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


def select(request, query):
    session = requests.Session()
    response = session.get(
        'https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q='+query)
    select_list = response.json()
    template = loader.get_template('locations/select.html')
    context = {
        'query': query,
        'select_list': select_list,
    }

    if request.method == "POST":
        index = request.POST.get('choice', False)
        if(index):
            selected_choice = select_list[int(index)]
            print(index)
            print(selected_choice)
            new_location = Location(addressZH=selected_choice['addressZH'],
                                    nameZH=selected_choice['nameZH'],
                                    x=selected_choice['x'],
                                    y=selected_choice['y'],
                                    nameEN=selected_choice['nameEN'],
                                    addressEN=selected_choice['addressEN'])
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
