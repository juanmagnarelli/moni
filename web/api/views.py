from django.shortcuts import render, redirect
from .models import cliente
from .forms import ClienteForm
from .config import URL_ENDPOINT, CREDENTIAL
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as do_login
import requests as r
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def pedidos(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            client = cliente.objects.get(id=request.POST['id'])
            client.delete()
        return render(request, 'pedidos.html', {'pedidos': cliente.objects.all()})
    # En otro caso redireccionamos al login
    return redirect('/login')
    

@csrf_protect
def solicitud(request):
    if request.method == "POST":
        client = ClienteForm(data=request.POST)
        error = True
        print(client.is_valid())
        if client.is_valid():
            client = client.save(commit=False)
            headers = {'credential': CREDENTIAL}
            res = r.get(URL_ENDPOINT + str(client.dni), headers=headers)
            if res.ok and res.status_code == 200:
                error = res.json()['has_error']
                client.status = True if res.json()['status'] == 'approve' else False
                client.save()

            return render(request, 'index.html', {"respuesta": True, "error": error, "status": client.status, "form": client})
        else:
            return render(request, "index.html", {"respuesta": True, "error":error, "form": client})
    else:
        return render(request, 'index.html', {"respuesta": False, 'form': ClienteForm()})

@csrf_protect
def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                return redirect('/solicitud')
    return render(request, "login.html", {'form': form})

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                do_login(request, user)
                return redirect('/solicitud')
        print(form.errors)
        print(form.non_field_errors)
    return render(request, "register.html", {'form': form})

