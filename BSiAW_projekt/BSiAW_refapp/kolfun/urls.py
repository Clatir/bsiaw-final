from django.urls import path
from . import views
urlpatterns = [
    path('kolmecze',views.kolmecze, name = 'kolmecze'),
    path('meczek/<int:mecz_id>/', views.szczegolymeczuk, name='szczegolymeczuk'),
    path('sprawozdaniek/<int:mecz_id>/',views.sprawozdaniek, name = 'sprawozdaniek'),
    path('sgospk/<int:mecz_id>/',views.sgospk, name = 'sgospk'),
    path('sgosck/<int:mecz_id>/',views.sgosck, name = 'sgosck'),
    path('eventk/<int:mecz_id>/',views.eventk, name = 'eventk'),
    path('addmecz/',views.addmecz, name = 'addmecz'),
    path('editusrk', views.editusrk, name = 'editusrk'),
]