from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from juwuegowosApp.models import User, Game
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout


def testView(request):
    return render(request, "test.html")


def home(request):  # the index view
    return render(request, "juwuegowosApp/index.html")


def register_user(request):
    if request.method == 'GET': #Si estamos cargando la página
     return render(request, "juwuegowosApp/register_user.html") #Mostrar el template

    elif request.method == 'POST': #Si estamos recibiendo el form de registro
     #Tomar los elementos del formulario que vienen en request.POST
     nombre = request.POST['nombre']
     contraseña = request.POST['contraseña']
     mail = request.POST['mail']
     imagen = request.POST['img-usuario']


     #Crear el nuevo usuario
     user = User.objects.create_user(username=nombre, password=contraseña, email=mail, picture=imagen)

     #Redireccionar la página /home
     return HttpResponseRedirect('/login')



def login_user(request):
    if request.method == 'GET':
        return render(request,"juwuegowosApp/login.html")
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['contraseña']
        usuario = authenticate(username=username,password=contraseña)
        if usuario is not None:
            login(request,usuario)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/register')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def play_game(request, game_id):
    game = Game.objects.filter(id=game_id)[0]
    return render(request, "juwuegowosApp/game_page.html", {"game": game})


def catalog(request):
    games = Game.objects.all()
    return render(request, "juwuegowosApp/catalogo.html", {"games": games})
