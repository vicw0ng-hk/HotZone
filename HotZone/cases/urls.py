from django.urls import path

from . import views

urlpatterns = [
    path('add', views.add, name='add'),
    path('add/patient', views.add_patient, name='add_patient'),
    path('add/virus', views.add_virus, name='add_virus'),
    path('add/location', views.add_location, name='add_location'),
    path('add/create_virus', views.create_virus, name='create_virus'),
    path('', views.main, name='main'),
    path('caselocation', views.caselocation, name='caselocation'),
    path('caselocation/add', views.caselocation_add, name='caselocation_add')
]
