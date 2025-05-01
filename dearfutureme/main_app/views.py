from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CapsuleForm
from .models import Capsule

# Create your views here.

def home(request):
    return render(request, 'home.html')

def capsule_page(request):
    capsules = Capsule.objects.filter(user=request.user)
    return render(request, 'capsules.html', {'capsules': capsules})

def capsule_create(request):
    if request.method == 'POST':
        form = CapsuleForm(request.POST, request.FILES)
        if form.is_valid():
            capsule = form.save(commit=False)
            capsule.user = request.user
            capsule.save()
            return redirect('capsules')
    else:
        form = CapsuleForm()
    return render(request, 'capsule_form.html', {'form': form})


def signup_view(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('capsules')
        else:
            error_message = 'Opp! There was an error with your signup. Please try again.'
    else:
        form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('capsules')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')