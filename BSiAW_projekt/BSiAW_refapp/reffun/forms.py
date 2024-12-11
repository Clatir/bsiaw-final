from django import forms
from game.models import Match, Zawodnik, Events

class EdytujMeczForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['wynik']

class DodajZawodnikaForm(forms.ModelForm):
    class Meta:
        model = Zawodnik
        fields = ['imie', 'nazwisko','nr']

class DodajEventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['typ','minuta','kto','nr_zawodnika']