from django.contrib import admin
from .models import Match, Klub, Zawodnik, Events
# Register your models here.
admin.site.register(Match)
admin.site.register(Klub)
admin.site.register(Zawodnik)
admin.site.register(Events)