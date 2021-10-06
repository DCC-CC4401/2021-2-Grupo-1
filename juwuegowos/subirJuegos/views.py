from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from juwuegowosApp.models import Game

# Create your views here.

def subir_juegos(request):
    if request.method == "POST":
        game_name = request.POST["game-name"]
        game_desc = request.POST["game-desc"]
        game_tags = request.POST["game-tags"]
        #game_url = request.POST.get("game-files",False)
        game_thmbnl = request.FILES['game-img']
        is_nsfw = request.POST.get("nsfw", False)=="on"
        dev = request.user
        #falta agregar los game_files, no se donde iria eso.
        game = Game(name=game_name, description=game_desc,thumbnail=game_thmbnl, nsfw=is_nsfw, developer=dev)
        game.save() 
        game.tags.add(game_tags) 
        game.save() 
        return HttpResponseRedirect("/") 
    else:    
        return render(request, 'template_subirJuegos/subir_juegos.html')    
    