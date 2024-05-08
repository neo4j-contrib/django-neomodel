from django.shortcuts import render
from .models import Data

# Create your views here.
def data_list(request):
    # data = Data.objects.all().order_by('-date')
    # return render(request, 'data/data_list.html', {'data': data})
    return render(request, 'data/data_list.html')

# def data_page (request, slug):
#     data = Data.objects.get(slug=slug)
#     return render(request, 'data/data_page.html', {'data': data})