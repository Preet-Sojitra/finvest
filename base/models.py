from email.policy import default
from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    

class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    topic=models.ForeignKey(Topic, on_delete = models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True) # auto_now_add will run every time the model is saved
    created = models.DateTimeField(auto_now_add=True) # auto_now_add only runs one when we created the object
    
    class Meta:
        ordering = ['-updated', '-created']  #newest one will be added first
    
    def __str__(self): 
        return self.name
    