from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class TypeUser(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')


class Profile(models.Model):
    #user = models.IntegerField(unique=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='user', null=True)