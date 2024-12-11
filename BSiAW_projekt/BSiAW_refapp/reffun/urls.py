from django.urls import path
from . import views
urlpatterns = [
    path('listameczy',views.listameczy, name = 'listameczy'),
    path('mecze/<int:mecz_id>/', views.szczegolymeczu, name='szczegolymeczu'),
    path('sprawozdanie/<int:mecz_id>/',views.sprawozdanie, name = 'sprawozdanie'),
    path('sgosp/<int:mecz_id>/',views.sgosp, name = 'sgosp'),
    path('sgosc/<int:mecz_id>/',views.sgosc, name = 'sgosc'),
    path('event/<int:mecz_id>/',views.event, name = 'event'),
    path('addevent/<int:mecz_id>/',views.addevent, name = 'addevent'),
    path('addzawodnikh/<int:mecz_id>/',views.addzawodnikh, name = 'addzawodnikh'),
    path('addzawodnika/<int:mecz_id>/',views.addzawodnika, name = 'addzawodnika'),
    path('editusr', views.editusr, name = 'editusr'),
]