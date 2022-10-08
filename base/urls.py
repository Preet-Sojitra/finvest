from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.loginPage, name="login"),

    path('', views.home, name='home'),
    # path('room/', views.room, name='room'),
    
    # passing dynamic data to the url
    path('room/<str:pk>/', views.room, name='room'), #pk stands for primaykey
    
    path('create-room/', views.createRoom, name='create-room'),
] 