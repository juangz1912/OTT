from django.db import models


# Create your models here.
from embed_video.fields import EmbedVideoField

class Item(models.Model):
    video = EmbedVideoField()  # same like models.URLField()

class Item2(models.Model):
    video = EmbedVideoField()  # same like models.URLField()    

class Item3(models.Model):
    video = EmbedVideoField()  # same like models.URLField() 

class Item4(models.Model):
    video = EmbedVideoField()  # same like models.URLField()     