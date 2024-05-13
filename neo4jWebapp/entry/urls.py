from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry, name="entry-page"),
    path('equipment/', views.equipment, name="equipment-page"),
    # path('lru/', views.lru, name="lru-page"),
    # path('port/', views.port, name="port-page"),
    # path('connector/', views.connector, name="conn-page"),
    # path('wire/', views.wire, name="wire-page"),
]