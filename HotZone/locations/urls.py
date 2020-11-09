from django.urls import path

from . import views

app_name = 'locations'
urlpatterns = [
    path('', views.index, name='index'),
    path('select/<str:query>', views.select, name='select'),
]
