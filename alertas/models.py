from __future__ import unicode_literals

from django.db import models

#Tipos de Amenazas - type threat
class TypeThreat(models.Model):
   name = models.CharField(max_length=100,unique=True)

   def __unicode__(self):
      return self.name

#Amenazas - threat
class Threat(models.Model):
   typeThreat = models.IntegerField()
   name = models.CharField(max_length=100)
   scientific_name = models.CharField(max_length=100)
   description = models.CharField(max_length=300)
   wikipedia_link =  models.CharField(max_length=400)
   active = models.BooleanField(default=True)
  
   def __unicode__(self):
      return self.name

#Detalle Amenaza - threat detail
class ThreatDetail(models.Model):
   typeCrop = models.IntegerField()
   threat = models.IntegerField()
   rango_alcance = models.IntegerField()
   expiracion = models.CharField(max_length=100)
  

class Detection(models.Model):
   user = models.IntegerField()
   threatDetail = models.BigIntegerField()
   activity = models.BigIntegerField()
   #location_id = models.CharField(max_length=100)
   #source = models.CharField(max_length=100)
   #source_score = models.CharField(max_length=100)
   date = models.CharField(max_length=100)
   damage_level = models.IntegerField()
   movil = models.BigIntegerField()
   location_lat = models.CharField(max_length=100)
   location_long = models.CharField(max_length=100)
	

class Seen(models.Model):
   user = models.IntegerField()
   object = models.BigIntegerField()
   object_type = models.CharField(max_length=100)
   date_time = models.CharField(max_length=100)
   
   def __unicode__(self):
      return self.object_type

class Note(models.Model):
   object = models.BigIntegerField()
   object_type = models.CharField(max_length=100)
   content = models.CharField(max_length=1000)
   user = models.IntegerField()
   
   def __unicode__(self):
      return self.object_type


class Picture(models.Model):
   object = models.BigIntegerField()
   object_type = models.CharField(max_length=100)
   image = models.ImageField(upload_to='img', null=True) 
   source = models.CharField(max_length=1000)
   
   def __unicode__(self):
      return self.object_type

