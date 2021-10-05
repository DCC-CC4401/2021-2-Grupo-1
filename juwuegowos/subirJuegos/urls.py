from django.urls import path
from . import views

urlpatterns = [
    path('upload-game/', views.subir_juegos)
]