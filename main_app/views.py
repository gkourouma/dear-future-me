from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CapsuleForm
from .models import Capsule, Memory, Comment
from .forms import CommentForm
from .forms import MemoryForm
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

@login_required
def profile_view(request):
    user = request.user
    profile = user.profile  
    capsules = user.capsules.all()
    memories = user.memories.all()

    context = {
        'profile': profile,
        'join_date': user.date_joined,
        'total_capsules': capsules.count(),
        'total_memories': memories.count(),
        'recent_activities': memories.order_by('-created_at')[:6],
    }
    return render(request, 'profile.html', context)

def search_user(request):
    query = request.GET.get("q")
    users = User.objects.filter(username__icontains=query) if query else []
    return render(request, "search_users.html", {"users": users, "query": query})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    capsules = user.capsules.all()
    memories = user.memories.all()
    context = {
        'user': user,
        'profile': profile,
        'join_date': user.date_joined,
        'total_capsules': capsules.count(),
        'total_memories': memories.count(),
        'recent_activities': memories.order_by('-created_at')[:6],
        'profile_owner': request.user == user,
    }
    return render(request, 'user_profile.html', context)

@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile_form.html', {'form': form, 'profile': profile})


@login_required
def profile_delete(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.user != profile.user:
        return redirect('profile') 
    if request.method == 'POST':
        profile.delete()
        return redirect('home')
    return render(request, 'edit_profile_form.html', {'profile': profile})

@login_required
def capsule_page(request):
    capsules = Capsule.objects.filter(user=request.user)
    return render(request, 'capsules.html', {'capsules': capsules, 'target_user': request.user})

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

def capsule_edit(request, capsule_id):
    capsule = get_object_or_404(Capsule, id=capsule_id, user=request.user)
    if request.method == 'POST':
        form = CapsuleForm(request.POST, request.FILES, instance=capsule)
        if form.is_valid():
            form.save()
            return redirect('capsule_detail', capsule_id=capsule.id)
    else:
        form = CapsuleForm(instance=capsule)
    return render(request, 'capsule_form.html', {'form': form, 'capsule': capsule})

def capsule_delete(request, capsule_id):
    capsule = get_object_or_404(Capsule, id=capsule_id, user=request.user)
    if request.method == 'POST':
        capsule.delete()
        return redirect('capsules')
    return render(request, 'capsule_delete.html', {'capsule': capsule})

def capsule_detail(request, capsule_id):
    capsule = get_object_or_404(Capsule, id=capsule_id)
    memories = capsule.memories.all()
    is_owner = request.user == capsule.user

    if capsule.is_locked and not capsule.is_unlockable():
        messages.warning(request, "This capsule is locked and cannot be opened until its unlock date.")
        return redirect('capsules')

    if request.method == 'POST' and is_owner:
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
        'form': form,
        'is_owner': is_owner,
    })


def user_capsules(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    capsules = Capsule.objects.filter(user=target_user)

    return render(request, 'capsules.html', {
        'capsules': capsules,
        'target_user': target_user
    })


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
    memory = get_object_or_404(Memory, id=memory_id)
    comments = memory.comments.all().order_by('-created_at')
    target_user = request.user == memory.user
    comment_form = CommentForm()
    return render(request, 'memory_detail.html', {
        'memory': memory,
        'comments': comments,
        'target_user': request.user,
        'comment_form': comment_form,
    })

def memory_delete(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id, user=request.user)
    if request.method == 'POST':
        memory.delete()
        return redirect('capsule_detail', capsule_id=memory.capsule.id)
    return render(request, 'memory_delete.html', {'memory': memory})

def memory_edit(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id, user=request.user)
    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES, instance=memory)
        if form.is_valid():
            form.save()
            return redirect('memory_detail', memory_id=memory.id)
    else:
        form = MemoryForm(instance=memory)
    return render(request, 'memory_form.html', {'form': form, 'memory': memory, 'capsule': memory.capsule})

def like_memory(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id)
    if request.user in memory.likes.all():
        memory.likes.remove(request.user)
    else:
        memory.likes.add(request.user)
    return redirect('memory_detail', memory_id=memory_id)

def add_comment(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.memory = memory
            comment.user = request.user
            comment.save()
    return redirect('memory_detail', memory_id=memory_id)

@login_required
@csrf_exempt
def save_avatar(request):
    if request.method == "POST":
        payload = json.loads(request.body)
        public_id = payload.get("public_id")
        if public_id:
            profile = request.user.profile
            profile.profile_picture = public_id
            profile.save()
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)


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