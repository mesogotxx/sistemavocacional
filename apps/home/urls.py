# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.perfil, name='home'),
    path('home/', views.index, name='home'),
    path('alumnos/', views.alumnos, name='alumnos'),
    path('notas/', views.notas, name='notas'),
    path('testvocacional/', views.testvocacional, name='testvocacional'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
