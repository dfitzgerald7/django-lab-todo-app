from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LabForm, TodoForm, TodoFormSet, TodoCheckboxForm
from django.forms import formset_factory
from django.forms import modelformset_factory
from .models import Todo, Lab
from django.db.models import Q
# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        completed = Lab.objects.filter(users=request.user, completed=True)
        incompleted = Lab.objects.filter(users=request.user, completed=False).order_by('due_date')
        print(incompleted)
        return render(request, 
                    'main/homepage.html',
                    context={'completed': completed, 'incompleted': incompleted,
                            'logged_in': True})
    else: 
        return render(request,
                      'main/homepage.html', 
                      {'logged_in': False})

def signup(request):
    if request.method == "POST":  
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            return redirect('main:homepage')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

    form = UserCreationForm
    return render(request, 
                  'main/signup.html',
                  context={'form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}')
                return redirect('main:homepage')
            else:
                messages.error(request, 'Invalid username or password')
        else: 
            messages.error(request, 'Invalid username or password. Likely missing a field.')
   
    form = AuthenticationForm
    return render(request, 
                  'main/login.html',
                  {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('main:homepage')

def new_lab(request):
    todo_formset = formset_factory(TodoForm)
    # todo_formset = modelformset_factory(Todo, fields=('title',))
    if request.method == "POST":
        form = LabForm(request.POST)
        todos_form = todo_formset(request.POST)
        if form.is_valid() & todos_form.is_valid():
            lab = form.save()
            lab.users.add(request.user)
           
            for todo_f in todos_form:
                if todo_f.is_valid():
                    todo = todo_f.save()
                    lab.todo_set.add(todo)
            return redirect('main:homepage')
        else: 
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")
    form = LabForm
    return render(request,
                  'main/labs/new.html',
                  {'form': form,
                    'todo_form': todo_formset
                  })
        
def lab_show(request, lab_id):
    lab = Lab.objects.get(pk=lab_id)
    completed = Todo.objects.filter(Q(lab__pk=lab_id) & Q(completed=True))
    todos = Todo.objects.filter(Q(lab__pk=lab_id) & Q(completed=False))



    checkbox_form = TodoCheckboxForm(lab)

    if request.method == "POST":
        form = TodoCheckboxForm(lab, request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            for todo in form.cleaned_data['todos']:
                todo.completed = True
                todo.save()
            

        lab.save()
        return redirect('main:homepage')

    return render(request, 'main/labs/show.html', 
                    context={'lab':lab, 'completed':completed, 'todos': todos, 'form': checkbox_form} )
