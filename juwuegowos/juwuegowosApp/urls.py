from django.urls import path
from . import views

urlpatterns = [
    path('home', views.register_user, name='home'),
    path('register', views.register_user, name='register_user'),
    path('login',views.login_user, name='login'),
    path('logout',views.logout_user, name='logout'),
]