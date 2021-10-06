from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from juwuegowosApp.models import Game
from django.core.files.storage import FileSystemStorage
import zipfile
from os import remove, mkdir

# Create your views here.

def subir_juegos(request):
    if request.method == "POST":
        game_name = request.POST["game-name"]
        game_desc = request.POST["game-desc"]
        game_tags = request.POST["game-tags"]
        game_thmbnl = request.FILES['game-img']
        is_nsfw = request.POST.get("nsfw", False)=="on"
        dev = request.user
        #falta agregar los game_files, no se donde iria eso.
        game = Game(name=game_name, description=game_desc,thumbnail=game_thmbnl, nsfw=is_nsfw, developer=dev)
        game.save() 
        game.tags.add(game_tags) 
        game.save() 

        #print(game_files)

        game_files = request.FILES["game-files"]
        fs = FileSystemStorage()
        file_path = f"games/{game.id}/{game_files.name}"
        mkdir(f"media/games/{game.id}")
        filename = fs.save(file_path, game_files)
        upload_gamefiles_to = fs.url(filename)

        with zipfile.ZipFile("media/" + file_path) as file:
            for fname in file.namelist():
                file.extract(fname, f"media/games/{game.id}")
        remove("media/" + file_path)

        return HttpResponseRedirect("/") 
    else:    
        return render(request, 'template_subirJuegos/subir_juegos.html')    
    