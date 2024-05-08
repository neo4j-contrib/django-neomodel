from django.urls import path
from . import views

urlpatterns = [
    path('userSignIn/', views.signIn, name='userSignIn'),
]