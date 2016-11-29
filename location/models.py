from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Location(models.Model):
    user = models.ForeignKey(User)
    type_object = models.CharField(max_length=100)  #parcel,farm,user
    object = models.BigIntegerField()
    order = models.IntegerField()
    lat = models.CharField(max_length=100)
    long = models.CharField(max_length=100)

    def __unicode__(self):
        return self.type_object


