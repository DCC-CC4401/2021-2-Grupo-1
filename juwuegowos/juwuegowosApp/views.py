from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from juwuegowosApp.models import User, Game, Comment
from juwuegowosApp.forms import Gameform
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.core.files.storage import FileSystemStorage
import zipfile
from os import remove, mkdir


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
        imagen = request.FILES['img-usuario']


        #Crear el nuevo usuario
        user = User.objects.create_user(username=nombre, password=contraseña, email=mail)
        #imagen = request.FILES['img-usuario']
        fs = FileSystemStorage()
        image_file_path = f"images/profilePictures/{user.id}.png"
        fs.save(image_file_path, imagen)

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


def game_comments(request, game_id):
    if request.method == "GET":
        comments = Comment.objects.filter(game_id=game_id)
        return render(request, "juwuegowosApp/comment_section.html", {"comments": comments})
    elif request.method == "POST":
        comment = request.POST["comment"]
        new_comment = Comment(comment=comment, game_id=game_id, user_id=0) #obtener la id del usuario
        new_comment.save()
        comments = Comment.objects.filter(game_id=game_id)
        return render(request, "juwuegowosApp/comment_section.html", {"comments": comments})

def editar_juego(request, game_id):
    game = Game.objects.filter(id=game_id)[0]
    form = Gameform(request.POST or None, instance= game)
    if form.is_valid():
        form.save()
        return redirect("catalogo")
    return render(request, "juwuegowosApp/editar_juego.html", {"game": game, 'form': form})