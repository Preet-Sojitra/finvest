from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('social-auth/', include('social_django.urls', namespace='social')),

    path('', views.home, name='home'),
    # path('room/', views.room, name='room'),
    
    # passing dynamic data to the url
    path('room/<str:pk>/', views.room, name='room'), #pk stands for primaykey
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    
    path('create-room/', views.createRoom, name='create-room'),
] 