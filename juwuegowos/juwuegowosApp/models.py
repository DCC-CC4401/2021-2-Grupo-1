from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    picture = models.ImageField(upload_to="images/profilePictures")

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=51000)
    date = models.DateField(default=timezone.now().strftime("%d/%m/%Y"))
    nsfw = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="images/thumbnails")

class Comment(models.Model):
    user_id = ForeignKey(User, on_delete=models.CASCADE)
    game_id = ForeignKey(Game, on_delete=models.CASCADE)
    comment = models.CharField(max_length=51000)
    date = models.DateTimeField(timezone.now().strftime("%d/%m/%Y - %H:%M"))

class Tag(models.Model):
    tag = models.CharField(max_length=50, primary_key=True)

class GameTag(models.Model):
    game_id = ForeignKey(Game, on_delete=models.CASCADE)
    tag = ForeignKey(Tag, on_delete=models.CASCADE)

class GameDeveloper(models.Model):
    user_id = ForeignKey(User, on_delete=models.CASCADE)
    game_id = ForeignKey(Game, on_delete=models.CASCADE)

class SocialMedia(models.Model):
    name = CharField(max_length=32)

class UserSocialMedia(models.Model):
    user_id = ForeignKey(User, on_delete=models.CASCADE)
    social_media = ForeignKey(SocialMedia, on_delete=models.CASCADE)
    username = CharField(max_length=255)