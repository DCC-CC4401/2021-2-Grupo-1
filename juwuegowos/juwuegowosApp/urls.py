from django.urls import path
from . import views

urlpatterns = [
    path('home', views.testView, name='home'),
    path('register', views.register_user, name='register_user'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path("", views.catalog, name="catalogo"),
    path("jugar/<int:game_id>", views.testView, name="jugar")
]

