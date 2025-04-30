from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.urls import path

# Create your views here.

def home(request):
    return render(request, 'home.html')

def capsules(request):
    return render(request, 'capsules.html')


def signup_view(request):
    if request.method == 'POST':
        # Handle the signup logic here
        pass
    return render(request, 'signup.html')
def login_view(request):
    if request.method == 'POST':
        # Handle the login logic here
        pass
    return render(request, 'login.html')
def logout_view(request):
    # Handle the logout logic here
    return render(request, 'logout.html')