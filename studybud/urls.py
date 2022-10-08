import imp
from django.contrib import admin
from django.urls import path, include
# from django.http import HttpResponse

# These two (home and room) are views
# views triggers url and thus we get response. 
# it is easier to put views in views.py

# def home(request):
#     return  HttpResponse('Home Page')

# def room(request):
#     return HttpResponse('Room')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')), # we tell django to include base.urls in our project instead of using admin urls
]
