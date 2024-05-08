from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SNCUser
from .forms import UserRegisterForm

def signIn(request):
    context = {
        'snc_users': SNCUser.objects.all(),
        'form':UserRegisterForm()
    }
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! You are now able to login.')
            return redirect('login')
        else:
            context['form'] = form      
    else:
        context['form'] = UserRegisterForm()
        
    return render(request, 'userSignIn/signInPage.html', context)

@login_required
def profile(request):
    return render(request, 'userSignIn/profile.html')