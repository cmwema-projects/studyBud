from .models import Topic, Room, Message
from django.forms import ModelForm


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class RoomCreationForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']