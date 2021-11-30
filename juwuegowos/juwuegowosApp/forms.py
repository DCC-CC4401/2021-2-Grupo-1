from django import forms
from django.forms import ModelForm
from .models import Game

class Gameform(ModelForm):
    class Meta:
        model = Game
        fields = ("name", "description", 'nsfw', "tags")
        required = ("name", "description")