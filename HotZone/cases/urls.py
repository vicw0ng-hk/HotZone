from django.urls import path

from . import views

urlpatterns = [
    path('add', views.add, name='add'),
    path('add/create_virus', views.create_virus, name='create_virus'),
    path('', views.main, name='main'),
    path('caselocation', views.caselocation, name='caselocation'),
    path('caselocation/add', views.caselocation_add, name='caselocation_add'),
    path('cluster', views.cluster, name='cluster'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_password_done/', views.change_password_done, name='change_password_done')
]
