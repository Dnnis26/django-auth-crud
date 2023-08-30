from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TasksForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:  # registrar usuario
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Contraseña no coinciden'
        })

@login_required
def tasks(request):
    #tasks = Task.objects.all() - Devuelve todas las tareas de la BD
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):
    
    if request.method =='GET':
         return render(request, 'create-tasks.html',{
            'form': TasksForm
        })
    else:
        try:
            form = TasksForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect(tasks)
        except ValueError: 
             return render(request, 'create-tasks.html',{
            'form': TasksForm,
            'error': "Provee datos validos"
        })
@login_required           
def task_detail(request, task_id):
    if request.method == 'GET':
        tasks = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TasksForm(instance=tasks)
        return render(request, 'tasks_detail.html', {'task': tasks, 'form': form} )
    else:
        try:
            tasks = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TasksForm(request.POST, instance=tasks)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks_detail.html', {'task': tasks, 'form': form, 'error':"Error actualizando"} )
        
def complete_task(request, task_id):
   tasks = get_object_or_404(Task, pk=task_id, user=request.user)
   if request.method == 'POST':
       tasks.datecompleted = timezone.now()
       tasks.save()
       return redirect('tasks')
   
@login_required 
def delete_task(request, task_id):
    tasks = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
       tasks.delete()
       return redirect('tasks')   
   
@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': "Usuario o contraseña incorrecto"
        })
        else:
            login(request, user)
            return redirect('tasks')
