from .models import Topic, Room, Message
from django.forms import ModelForm


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

