from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import UserUpdateForm

from django.http import HttpResponse
#TODO: creo que habria que crear clases casi para cada vista

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, " ¡ Bienvenido "+username+" !")
            request.session['username'] = username
            return redirect('../')
            # Redirect to a success page.
        else:
            # return redirect(request.path)
            messages.error(request, " ¡Error al iniciar sesión! Comprueba que tus credenciales sean correctas...")
            return render(request, 'user/login.html',{})
    else: 
        return render(request, 'user/login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, " Has cerrado sesión")
    return redirect('../')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request,user)
            request.session['username'] = username
            messages.success(request, " ¡Te has registrado con éxito!")
            return redirect('../')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html',{'form':form})

def profile(request, username):
    request.session['username'] = request.user.username
    try:
        user = User.objects.get(username=username)
        
    except User.DoesNotExist:
        Exception("El usuario no existe")

    return render(request, 'user/profile.html',{'user':user})

def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            user = request.user
            request.session['username'] = user.username
            messages.success(request, "Tus datos se han guardado con éxito!")
            return render(request, 'user/profile.html',{'user':user})
    else: 
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form':u_form
    }
    return render(request, 'user/edit_profile.html', context)
