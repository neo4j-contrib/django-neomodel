from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
    path('data/', views.data_list, name="data-page"),
    # path('<slug:slug>', views.data_page, name="data-page-slug"),
]