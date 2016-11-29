from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from mapeo.models import TypeCrop, Activity


#Tipos de Amenazas - type threat
class TypeThreat(models.Model):
   name = models.CharField(max_length=100,unique=True)

   def __unicode__(self):
      return self.name

#Amenazas - threat
class Threat(models.Model):
   typeThreat = models.ForeignKey(TypeThreat)
   name = models.CharField(max_length=100)
   scientific_name = models.CharField(max_length=100)
   description = models.CharField(max_length=300)
   wikipedia_link =  models.CharField(max_length=400)
   active = models.BooleanField(default=True)
  
   def __unicode__(self):
      return self.name

#Detalle Amenaza - threat detail
class ThreatDetail(models.Model):
   typeCrop = models.ForeignKey(TypeCrop)
   threat = models.ForeignKey(Threat)
   rango_alcance = models.IntegerField()
   expiracion = models.CharField(max_length=100)

   def __str__(self):
      return "{1} - {0}".format(self.typeCrop, self.threat)
  

class Detection(models.Model):
   user = models.ForeignKey(User)
   threatDetail = models.ForeignKey(ThreatDetail)
   activity = models.ForeignKey(Activity)
   #location_id = models.CharField(max_length=100)
   #source = models.CharField(max_length=100)
   #source_score = models.CharField(max_length=100)
   date = models.CharField(max_length=100)
   damage_level = models.IntegerField()
   movil_id = models.BigIntegerField(primary_key=True)
   location_lat = models.CharField(max_length=100)
   location_long = models.CharField(max_length=100)
	

class Seen(models.Model):
   user = models.ForeignKey(User)
   object = models.BigIntegerField()
   object_type = models.CharField(max_length=100)
   date_time = models.CharField(max_length=100)
   
   def __unicode__(self):
      return self.object_type

class Note(models.Model):
   object = models.BigIntegerField()
   object_type = models.CharField(max_length=100)
   content = models.CharField(max_length=1000)
   user = models.ForeignKey(User)
   
   def __unicode__(self):
      return self.object_type


class Picture(models.Model):
   object = models.BigIntegerField()
   object_type = models.CharField(max_length=100)
   image = models.ImageField(upload_to='img', null=True) 
   source = models.CharField(max_length=1000)
   
   def __unicode__(self):
      return self.object_type


#class Object(models.Model):
   #type = models.CharField()