from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CapsuleForm
from .models import Capsule, Memory
from .forms import MemoryForm
from django.contrib.auth.decorators import login_required

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

def capsule_detail(request, capsule_id):
    capsule = Capsule.objects.get(id=capsule_id)
    memories = capsule.memories.all()
    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.user = request.user
            memory.capsule = capsule
            memory.save()
            return redirect('capsule_detail', capsule_id=capsule.id)
    else:
        form = MemoryForm()

    return render(request, 'capsule_detail.html', {
        'capsule': capsule,
        'memories': memories,
        'form': form})


def add_memory(request, capsule_id):
    capsule = get_object_or_404(Capsule, id=capsule_id, user=request.user)
    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.user = request.user
            memory.capsule = capsule
            memory.save()
            return redirect('capsule_detail', capsule_id=capsule.id)
    else:
        form = MemoryForm()
    return render(request, 'memory_form.html', {'form': form, 'capsule': capsule})

def memory_detail(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id, user=request.user)
    return render(request, 'memory_detail.html', {'memory': memory})

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