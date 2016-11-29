from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    mobile_id = models.IntegerField(unique=True)


##Modelos para realizar MAPEO

#Farm (campos)
class Farm(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    movil_id = models.BigIntegerField(unique=True)
    #dateLastModification = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
        #def validate(self, request):
        #    key = request.user
        #    raise serializers.ValidationError(("nada"))



#Parcel (parcelas)
class Parcel(models.Model):
    #id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    farm = models.ForeignKey(Farm)
    name = models.CharField(max_length=100)
    surface = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    center_lat = models.CharField(max_length=100)
    center_long = models.CharField(max_length=100)
    movil_id = models.BigIntegerField(unique=True)
    
    def __unicode__(self):
        return self.name

# Cultivos - type crop
class TypeCrop(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

#Actividades en parcelas
class Activity(models.Model):
    user = models.ForeignKey(User)
    parcel = models.ForeignKey(Parcel)
    typeCrop = models.ForeignKey(TypeCrop)
    campaign = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    movil_id = models.BigIntegerField(unique=True)

    def __unicode__(self):
        return self.campaing






