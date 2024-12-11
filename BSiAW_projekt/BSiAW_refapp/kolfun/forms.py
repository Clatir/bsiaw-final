from django import forms
from game.models import Match

class DodajMeczForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['Gosp', 'Gosc', 'SedziaG','SedziaA1', 'SedziaA2','data', 'godzina', 'ulica', 'miejscowosc','rozgrywki','runda','kolejka']