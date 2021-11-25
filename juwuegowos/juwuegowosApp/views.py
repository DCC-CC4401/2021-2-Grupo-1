from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseNotModified
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from juwuegowosApp.models import User, Game, Comment
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.core.files.storage import FileSystemStorage
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
        print(game_name)
        print(tags)
        print(dev_user)
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
    game = Game.objects.filter(id=game_id)[0]
    return render(request, "juwuegowosApp/game_page.html", {"game": game})


def catalog(request):
    limit = 6
    games = Game.objects.all()
    games_by_date = games.order_by('date')
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
