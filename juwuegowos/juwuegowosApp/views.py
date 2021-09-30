from django.http import HttpResponseRedirect
from juwuegowosApp.models import User
from django.shortcuts import render

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
     imagen = request.POST['imagen']


     #Crear el nuevo usuario
     user = User.objects.create_user(username=nombre, password=contraseña, email=mail, img=imagen)

     #Redireccionar la página /home
     return HttpResponseRedirect('/home')

from django.contrib.auth import authenticate, login,logout
def login_user(request):
    if request.method == 'GET':
        return render(request,"juwuegowosApp/login.html")
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['contraseña']
        usuario = authenticate(username=username,password=contraseña)
        if usuario is not None:
            login(request,usuario)
            return HttpResponseRedirect('/home')
        else:
            return HttpResponseRedirect('/register')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/home')

