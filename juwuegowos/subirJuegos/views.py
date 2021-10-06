from django.shortcuts import render
from django.http import HttpResponse
from juwuegowosApp.models import Game

# Create your views here.

def subir_juegos(request):
    if request.method == "POST":
        game_name = request.POST["game-name"]
        game_desc = request.POST["game-desc"]
        game_tags = request.POST["game-tags"]
        game_url = request.POST.get("game-files",False)
        game_thmbnl = request.POST["game-img"]
        is_nsfw = request.POST.get("nsfw", False)=="on"
        dev = request.user
        #esta porcion de codigo es la que genera el error
        #actualmente dice que juegosApp_game table no existe y muere
        #al intentar publicar 
        game = Game(name=game_name, description=game_desc,thumbnail=game_thmbnl, nsfw=is_nsfw, developer=dev) #crea la tupla
        game.save() #guarda la tupla en la tabla game para que se cree la primary key
        game.tags.add(game_tags) #ahora es posible editar los tags asi que se añaden
        game.save() #se vuelve a guardar con los tags añadidos
        return HttpResponse("/") #por ahora redirige a un msje, eventualmente redirigira a /mis juegos/
    else:    
        return render(request, 'template_subirJuegos/subir_juegos.html')    
    