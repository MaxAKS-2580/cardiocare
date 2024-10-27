from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns=[
    
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('data', views.data, name='data' ),
    path('dashboard', views.dashboard, name='dashboard'),
    path('data/', views.health_data_view, name='data'),
    path('ai', views.ai, name='ai')
]