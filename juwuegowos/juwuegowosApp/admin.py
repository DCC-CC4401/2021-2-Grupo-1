from django.contrib import admin

# Register your models here.
from juwuegowosApp.models import  User, Game, Comment

admin.site.register(User)
admin.site.register(Game)
admin.site.register(Comment)