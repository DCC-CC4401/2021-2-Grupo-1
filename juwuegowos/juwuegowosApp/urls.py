from django.conf.urls import url
from django.urls import path
from . import views
from juwuegowos.settings import STATIC_URL

urlpatterns = [
    path("", views.catalog, name="catalogo"),
    path('home', views.testView, name='home'),
    path('register', views.register_user, name='register_user'),
    path('login',views.login_user, name='login'),
    path('logout',views.logout_user, name='logout'),
    path("catalogo", views.testView, name="catalogo"),
    path("jugar/<int:game_id>/", views.play_game, name="jugar"),
    path("juego/<int:game_id>/", views.game, name="juego"),
]
