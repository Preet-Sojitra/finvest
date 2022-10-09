from django.forms import ModelForm
from .models import Room, Image

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' 

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ("name", "img")