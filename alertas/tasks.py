# -*- coding: UTF8 -*-
from harry.celery import app

from celery import shared_task

from models import ThreatDetail,Threat,TypeThreat,Detection,Seen,Note,Picture
from mapeo.models import Activity, Parcel,TypeCrop
from pushes.models import Device
from pushes.views import push_notifications_view

from rest_framework import viewsets
from serializers import TypeThreatSerializer, ThreatDetailSerializer, ThreatSerializer, DetectionSerializer

#app.task
@app.task
def sendPush(amenaza_id):
    idA=0
    cultivo_id = 0
    lista_usuarios_cultivos = []
    #detalleAmenaza = ThreatDetail.objects.get(id=amenaza_id)
    #for objectDetalleAmenaza in detalleAmenaza:
    detalle = ThreatDetail.objects.get(id=amenaza_id)
    #for objectThreatDetail in detalle:
    idA = detalle.threat_id
    cultivo_id = detalle.typeCrop_id

    if(cultivo_id != 0):
        actividades = Activity.objects.filter(type_crop_id=cultivo_id)
        for objectActividades in actividades:
                usuario_id = objectActividades.user_id
                lista_usuarios_cultivos.append(usuario_id)

    cantidad = Detection.objects.filter(threatDetail_id=amenaza_id).count()

    data_message = {"type": 1, "threat_id": amenaza_id, "cantidad": cantidad}
    #data_message = {"title": "Se aproxima nombre_amenaza", "body" : "nuevas detecciones en tu zona", "type": 1, "threat_id": amenaza_id, "cantidad": cantidad}
    #detalle = ThreatDetail.objects.filter(id=amenaza_id)
    #for objectThreatDetail in detalle:
    #   idA = objectThreatDetail.threat_id
    amenaza = Threat.objects.get(id=idA)
    nombre_amenaza = amenaza.name
    #print nombre_amenaza
    if(len(lista_usuarios_cultivos)>0):
        for objectUsuario in lista_usuarios_cultivos:
                dispositivos = Device.objects.filter(user_id=objectUsuario,active=True)
                for objectDevice in dispositivos:
                        key_firebase = objectDevice.key_firebase
                        title = "Se aproxima " + nombre_amenaza + str("!")
                        body = str("1 Nueva detección en tu zona")
                        resultado = push_notifications_view(key_firebase, title, body,data_message)
 
