from django.conf.urls import url
from django.urls import path
from . import views
from juwuegowos.settings import STATIC_URL, MEDIA_ROOT, STATIC_ROOT
from django.conf.urls import handler400, handler403, handler404, handler500
from django.views.static import serve


urlpatterns = [
    path("", views.catalog, name="catalogo"),
    path('home', views.testView, name='home'),
    path('register', views.register_user, name='register_user'),
    path('login',views.login_user, name='login'),
    path('logout',views.logout_user, name='logout'),
    path("catalogo", views.testView, name="catalogo"),
    path("jugar/<int:game_id>/", views.play_game, name="jugar"),
    path("editar/<int:game_id>/", views.editar_juego, name="editar_juego"),
    path("search_results", views.search_results, name="search_results"),
    path("comments/<int:game_id>/<int:page>/<int:order>/", view=views.game_comments, name="comments"),
    path("comments/<int:game_id>/", view=views.post_comment, name="post_comment"),
    path("u/<int:user_id>/datos", view=views.edit_account, name="edit_account"),
    path("u/<int:user_id>/juegos", view=views.user_games, name="user_games"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': STATIC_ROOT}), 
]

handler404 = "juwuegowosApp.views.view404"
handler500 = "juwuegowosApp.views.view404"
handler403 = "juwuegowosApp.views.view404"
handler400 = "juwuegowosApp.views.view404"
