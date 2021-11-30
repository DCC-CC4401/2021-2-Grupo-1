from os import error, path
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, HttpResponseNotFound, HttpResponseNotModified
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from juwuegowosApp.models import User, Game, Comment
from juwuegowosApp.forms import Gameform
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.core.files.storage import FileSystemStorage
import zipfile
import os, shutil
from django.db.models import Q




def testView(request):
    return render(request, "test.html")

def search_results(request):
    if request.method == "POST":
        searched = request.POST["search"]
        if searched == '': 
            return HttpResponseRedirect("/")
        #parsing the string to filter
        #pasarlo todo a palabras separadas por espacios
        game_name, tags, dev = parse(searched)
        dev_user = User.objects.filter(username__contains=dev)
        games = Game.objects.all()
        if tags:
            games = games.filter(tags__name__in=tags)
        if game_name:
            games = games.filter(name__contains=game_name)
        if dev_user:
            games = games.filter(developer__in=dev_user)

        passed = {'searched' : searched, 'game_search': games}   
        return render(request, "juwuegowosApp/search_results.html", passed)

def parse(search):
    word_list = search.replace(',',' ').replace(';',' ').split()
    name_w = []
    tags = []
    dev = ''
    for w in word_list:
        if '#' in w:
            tags += [w[1:]]
        elif '@' in w:
            dev = w[1:]
        else:
            name_w += [w]
    name = ' '.join(name_w)
    return name, tags, dev
        
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
    if request.method == "GET":
        games = Game.objects.filter(id=game_id)
        if len(games) > 0:
            game = games[0]
            return render(request, "juwuegowosApp/game_page.html", {"game": game})
        raise Http404()


def catalog(request):
    limit = 6
    games = Game.objects.all()
    games_by_date = games.order_by('date')[::-1]
    games_by_random = games.order_by('?')
    games_featured = games.filter(name__in=['Una Marraqueta','Wi-Fi for Wanderers', 'Troubleshooters'])
    #games_featured = games
    return render(request, "juwuegowosApp/catalogo.html", {
        "games_featured": games_featured[:limit],
        "games_by_date": games_by_date[:limit],
        "games_by_random": games_by_random[:limit]
    })


def game_comments(request, game_id, page, order):
    if request.method == "GET":
        game = Game.objects.filter(id=game_id)[0]
        cond = "-" if order == 1 else ""
        comments = Comment.objects.filter(game_id=game).order_by(f"{cond}date")[page*15:(page+1)*15]
        if len(comments) > 0:
            return render(request, "juwuegowosApp/comment_section.html", {"comments": comments, "game": game})
        return HttpResponseNotModified()

def post_comment(request, game_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        game = Game.objects.filter(id=game_id)[0]
        new_comment = Comment(comment=comment, game_id=game, user_id=request.user)
        new_comment.save()
        return HttpResponseNotModified()

def editar_juego(request, game_id):
    if request.method == "GET":
        game = Game.objects.filter(id=game_id)[0]
        if request.user != game.developer:
            raise Http404()
        form = Gameform(None, instance= game)
        return render(request, "juwuegowosApp/editar_juego.html", {"game": game, 'form': form})
    elif request.method == "POST":
        game = Game.objects.filter(id=game_id)[0]
        if request.user != game.developer:
            raise Http404()
        form = Gameform(request.POST or None, instance= game)
        if form.is_valid():
            form.save()
            if "game-files" in request.FILES:
                game_files = request.FILES["game-files"]
                fs = FileSystemStorage()
                folder = f"media/games/{game.id}/"
                zip_path = f"games/{game.id}/{game_files.name}"
                shutil.rmtree(folder)
                os.mkdir(folder)

                filename = fs.save(zip_path, game_files)

                with zipfile.ZipFile("media/" + zip_path) as file:
                    for fname in file.namelist():
                        file.extract(fname, f"media/games/{game.id}")
                os.remove("media/" + zip_path)

            if "game-img" in request.FILES:
                game_thmbnl = request.FILES["game-img"]
                fs = FileSystemStorage()
                image_file_path = f"images/games/{game.id}/thumbnail.png"
                fs.save(image_file_path, game_thmbnl)
            return render(request, "juwuegowosApp/editar_juego.html", {"game": game, 'form': form})    
        return render(request, "juwuegowosApp/editar_juego.html", {"game": game, 'form': form})

def user_games(request, user_id):
    user = User.objects.filter(id=user_id)
    if len(user) == 0 or request.user != user[0]:
        raise Http404()
    if request.method == "GET":
        games = Game.objects.filter(developer=request.user)
        passed = {'game_search': games}
        return render(request, "juwuegowosApp/mis_juegos.html", passed)

def edit_account(request, user_id):
    user = User.objects.filter(id=user_id)
    if len(user) == 0 or request.user != user[0]:
        raise Http404()
    if request.method == "GET":
        return render(request, "juwuegowosApp/editar_datos.html")
    elif request.method == "POST":
        password_changed = False
        err = {"password": "", "username": ""}
        if len(request.POST["contraseña"]) >= 4 and request.POST["contraseña"] == request.POST["conf-contraseña"]:
            user[0].set_password(request.POST["contraseña"])
            password_changed = True
        user[0].email = request.POST["mail"]
        user[0].save()
        if "img-usuario" in request.FILES:
            imagen = request.FILES["img-usuario"]
            fs = FileSystemStorage()
            image_file_path = f"images/profilePictures/{user.id}.png"
            fs.save(image_file_path, imagen)
        if password_changed:
            return HttpResponseRedirect('/login')
        return render(request, "juwuegowosApp/editar_datos.html", err)
    

def view404(request, e):
    raise Http404()

def view500(request, e):
    raise Http404()

def view403(request, e):
    raise Http404()

def view400(request, e):
    raise Http404()

