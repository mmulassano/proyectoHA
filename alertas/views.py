# -*- coding: utf-8 -*- 
from django.shortcuts import render
from models import ThreatDetail,Threat,TypeThreat,Detection,Seen,Note,Picture
from mapeo.models import Activity, Parcel,TypeCrop
from pushes.models import Device
from pushes.views import push_notifications_view

from rest_framework import viewsets
from serializers import TypeThreatSerializer, ThreatDetailSerializer, ThreatSerializer, DetectionSerializer,NoteSerializer,PictureSerializer,SeenSerializer

from rest_framework.decorators import api_view
from rest_framework import viewsets, request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.http import HttpResponse
from django.db import transaction, IntegrityError
from pyfcm import FCMNotification


from harry import settings

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from django.core.exceptions import ObjectDoesNotExist
import datetime
import random

#...........
from django.contrib.auth import get_user_model
UserModel = get_user_model()
import json


from tasks import sendPush

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class TypeThreatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TypeThreat.objects.all().order_by()
    serializer_class = TypeThreatSerializer



class ThreatViewSet(viewsets.ModelViewSet):
    queryset = Threat.objects.all().order_by()
    serializer_class = ThreatSerializer


#Calculos 
from math import sin, cos, sqrt, asin, pi

def distanciakm(lat1, long1, lat2, long2):
    lat1 = float(lat1)
    long1 = float(long1)
    lat2 = float(lat2)
    long2 = float(long2)
    r = 6371000  # radio terrestre medio, en metros
    c = pi / 180  # constante para transformar grados en radianes
    d = 2 * r * asin(
        sqrt(
            sin(c * (lat2 - lat1) / 2) ** 2 + cos(c * lat1) * cos(c * lat2) * sin(c * (long2 - long1) / 2) ** 2))
    distancia = float(d / 1000)
    return  int(distancia)  # float("{0:.0f}".format(distancia))

#Promedio de la valorizacion de daño dada por el usuario
def promedioVU(list_damage_level):
    VA = -1
    sum = 0

    for i in range(0, len(list_damage_level)):
        sum = sum + list_damage_level[i]
        VA = (sum / len(list_damage_level))-1

    return int(VA)

def valorizacionVA(DistanciaMin,TipoAmenaza,CantDetecciones):
    D = DistanciaMin
    a=1
    C = CantDetecciones
    VA = 0

    if TipoAmenaza == 2:
        a = 15#Peste
    elif TipoAmenaza == 1:
        a = 10  # Plaga
    else:
        a = 5  #Maleza

    x = 0.6*D*a
    y = (0.4*C)
    z = x+y
    #valor = float("{0:.2f}".format(z))
    valor = D

    if valor <= 10 and valor >0:
        VA = 4
    elif valor > 10  and valor <= 30:
        VA = 3
    elif valor >30  and valor <= 60:
        VA = 2
    elif valor >60  and valor <=90:
        VA = 1
    else:
	VA = 0

    return VA





##########AMENAZAS
##################################
#consulta de las amenazas,
@api_view(['GET'])
def threat(request):
    if request.method == 'GET':
       #threats = Threat.objects.filter()
       #serializer = ThreatSerializer(threats, many=True)
       threatDetails = ThreatDetail.objects.filter()
       list_threat = []

       for objectThreatDetail in threatDetails:
           #serializer = ThreatSerializer(objectThreat)
            id_threat=objectThreatDetail.threat_id
            threats = Threat.objects.filter(id=id_threat)
            for objectThreat in threats:
                name = objectThreat.name
                scientific_name= objectThreat.scientific_name
                description = objectThreat.description
                wikipedia_link = objectThreat.wikipedia_link

            datatime = ""
            distance_min = 0
            valorization = 0
            sum_detection=0
            sum_seen = 0
            image_url='sin imagen'
            fuente='sin fuente'
            menor = 100000
            x_user = 0
            y_user = 0
            x_par = 0
            y_par = 0
            distancia=0
            list_distancias = []
	    distancias_ordenadas = []
            list_damage_level = []

            #parcels = Parcel.objects.filter(user_id=request.user.id)
            #for objectParcel in parcels:
            # x_user = float(objectParcel.center_lat)
            # y_user = float(objectParcel.center_long)


            detection = Detection.objects.filter(threatDetail_id=objectThreatDetail.id)
            for objectDetection in detection:
                sum_detection = sum_detection +1
                datatime = objectDetection.date
                id_actividad = objectDetection.activity_id
		list_damage_level.append(objectDetection.damage_level)

                if(id_actividad == 0):
                    x_par = objectDetection.location_lat
                    y_par = objectDetection.location_long
			
		    parcels = Parcel.objects.filter(user_id=request.user.id)
                    for objectParcel in parcels:                        
                        cant_act = Activity.objects.filter(parcel_id=objectParcel.movil_id,type_crop_id=objectThreatDetail.typeCrop_id).count()
                        if cant_act > 0:
                            x_user = float(objectParcel.center_lat)
                            y_user = float(objectParcel.center_long)

                            distancia = distanciakm(x_par, y_par, x_user, y_user)
                            if distancia > 0.0:
                            	list_distancias.append(distancia)
				

                else:
                    actividades = Activity.objects.filter(movil_id=id_actividad,type_crop_id = objectThreatDetail.typeCrop_id)
                    for objectActividades in actividades:
                        parcels = Parcel.objects.filter(movil_id=objectActividades.parcel_id)
                        for objectParcel in parcels:
                            x_par = float(objectParcel.center_lat)
                            y_par = float(objectParcel.center_long)
                
                	    parcels = Parcel.objects.filter(user_id=request.user.id)
                            for objectParcel in parcels:
                                cant_act = Activity.objects.filter(parcel_id=objectParcel.movil_id,type_crop_id=objectThreatDetail.typeCrop_id).count()
                                if cant_act > 0:
                                    x_user = float(objectParcel.center_lat)
                                    y_user = float(objectParcel.center_long) 
			            distancia = distanciakm(x_par,y_par,x_user,y_user)
                                    if distancia > 0.0:
				   	 list_distancias.append(distancia)
                         
	    
	    distancias_ordenadas = sorted(list_distancias)
            
	    if len(distancias_ordenadas) != 0:
		distance_min = distancias_ordenadas.pop(0)

	    #del distancias_ordenadas
	    #del list_distancias


            valorization =  promedioVU(list_damage_level)
            
            picture = Picture.objects.filter(object_id=id_threat, object_type="threat")
            for objectPicture in picture:
            	image = str(objectPicture.image)
                if (image != ""):
                	image_url = settings.MEDIA_URL + image
                        fuente = objectPicture.source
                else:
                        image_url = "sin imagen"

        
	    seens = Seen.objects.filter(object_id=objectThreatDetail.id, object_type="threat")
            for objectSeen in seens:
            	sum_seen = sum_seen + 1


            dato = {
		    "listas":distancias_ordenadas,
                    "threat_id":objectThreatDetail.id,
                    "name": name,
                    "scientific_name": scientific_name,
                    "description": description,
                    "wikipedia_link": wikipedia_link,
                    "typeThreat_id":objectThreat.typeThreat_id,
                    "crop_id": objectThreatDetail.typeCrop_id,
                    "detection_sum": sum_detection,
                    "seen_sum": sum_seen,
                    "image": image_url,
                    "datetime_last": datatime,
                    "distance_min": distance_min,
                    "valorization": valorization,
		    "source":fuente
                }
            list_threat.append(dato)

            
       return JSONResponse(list_threat)




#Agrega AMENAZA
@api_view(['POST'])
def threatNew(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():

                datos_threat= {}
                datos_threatDetail = {}
                datos_detection = {}
                datos_note = {}

                threat_id = 0
                threat = Threat.objects.filter(name=request.POST['name'],scientific_name=request.POST['scientific_name'])
                if (threat.count() > 0):
                    for objectThreat in threat:
                        threat_id = objectThreat.id
                else:
                    threat = Threat.objects.filter(scientific_name=request.POST['scientific_name'])
                    if(threat.count() > 0):
                        for objectThreat in threat:
                            threat_id = objectThreat.id
                    else:
                        threat = Threat.objects.filter(name=request.POST['name'])
                        if (threat.count() > 0):
                            for objectThreat in threat:
                                threat_id = objectThreat.id

                if(threat_id != 0):
                    #ver si existe el detalle
                    existe= ThreatDetail.objects.filter(threat_id=threat_id,typeCrop_id=request.POST['crop_id']).count()
                    #si exite, registro deteccion
                    if (existe !=  0):
			threatDetail=ThreatDetail.objects.filter(threat_id=threat_id,typeCrop_id=request.POST['crop_id'])
                        for objectThreatDetail in threatDetail:
                            threatDetail_id = objectThreatDetail.id
                            request.POST['threat_id'] = threatDetail_id

                            #inicio deteccion
			    datos_detection = {}
                            datos_note = {}

                            movil_id = request.POST['movil_id']

                            datos_detection['user_id'] = request.user.id
                            datos_detection['movil_id'] = movil_id
                            datos_detection['date'] = request.POST['date']
                            datos_detection['damage_level'] = request.POST['damage_level']
                            datos_detection['threatDetail_id'] = request.POST['threat_id']

                            datos_note['user_id'] = request.user.id
                            datos_note['object_id'] = movil_id
                            datos_note['object_type'] = "Detection"
                            datos_note['content'] = request.POST['note']

                            actividades = request.POST['activity_id']
                            actividades2 = actividades.replace("\\", "")
                            actividades_json = json.loads(actividades2)

                            for registroActividad in actividades_json:
                                activity_id = registroActividad['id']
                                datos_detection['activity_id'] = activity_id
                                datos_detection['location_lat'] = registroActividad['location_lat']
                                datos_detection['location_long'] = registroActividad['location_long']

                                existen = 0
                                if (activity_id == 0):
                                    # existen = 0
                                    existen = Detection.objects.filter(movil_id=movil_id,
                                                                       location_lat=datos_detection['location_lat'],
                                                                       location_long=datos_detection[
                                                                           'location_long']).count()
                                else:
                                    existen = Detection.objects.filter(movil_id=movil_id,
                                                                       activity_id=activity_id).count()

                                if (existen == 0):  
                                    serializer = DetectionSerializer(data=datos_detection)
                                    if serializer.is_valid():
                                        
                                        serializer.save()
                                        nota(datos_note)
                                        image(request)
                                        # PUSH envio notificacion
                                        push(datos_detection['threatDetail_id'])
                                        continue
                                    else:
                                        raise AttributeError

                                else:
                                    continue
				
                            #detection(request.data)
                            ##Fin deteccion

                    else:
                        #agrego detalle amenaza, aun no cargo la deteccion
                        datos_threatDetail['rango_alcance'] = 100
                        datos_threatDetail['threat_id'] = threat_id
                        datos_threatDetail['expiracion'] = "20170323"
                        datos_threatDetail['typeCrop_id'] = request.POST['crop_id']
                        serializer = ThreatDetailSerializer(data=datos_threatDetail)
                        if serializer.is_valid():
                        	serializer.save()
			    
                        else:
                        	raise AttributeError
			#cargo la deteccion por ahora
                        threatDetail=ThreatDetail.objects.filter(threat_id=threat_id,typeCrop_id=request.POST['crop_id'])
                        for objectThreatDetail in threatDetail:
                        	threatDetail_id = objectThreatDetail.id
                                request.POST['threat_id'] = threatDetail_id
                        	#detection(request.data)
				datos_detection = {}
                            	datos_note = {}

                           	movil_id = request.POST['movil_id']

                            	datos_detection['user_id'] = request.user.id
                           	datos_detection['movil_id'] = movil_id
                            	datos_detection['date'] = request.POST['date']
                            	datos_detection['damage_level'] = request.POST['damage_level']
                            	datos_detection['threatDetail_id'] = request.POST['threat_id']

                           	datos_note['user_id'] = request.user.id
                            	datos_note['object_id'] = movil_id
                            	datos_note['object_type'] = "Detection"
                            	datos_note['content'] = request.POST['note']

                            	actividades = request.POST['activity_id']
                            	actividades2 = actividades.replace("\\", "")
                            	actividades_json = json.loads(actividades2)

                            	for registroActividad in actividades_json:
                                	activity_id = registroActividad['id']
                                	datos_detection['activity_id'] = activity_id
                                	datos_detection['location_lat'] = registroActividad['location_lat']
                                	datos_detection['location_long'] = registroActividad['location_long']

                                	existen = 0
                                	if (activity_id == 0):
                                    		existen = Detection.objects.filter(movil_id=movil_id,location_lat=datos_detection['location_lat'],location_long=datos_detection['location_long']).count()
                                	else:
                                    		existen = Detection.objects.filter(movil_id=movil_id,activity_id=activity_id).count()

                                	if (existen == 0):
                                    		serializer = DetectionSerializer(data=datos_detection)
                                    		if serializer.is_valid():
                                        		serializer.save()
                                        		nota(datos_note)
                                        		image(request)
                                        		# PUSH envio notificacion
                                        		push(datos_detection['threatDetail_id'])
                                        		continue
                                    		else:
                                        		raise AttributeError

                                	else:
                                    		continue

                else:
                    # agregar la amenaza inactiva porque un admin debe activarla
                    datos_threat['movil_id'] = request.POST['movil_id']
                    datos_threat['name'] = request.POST['name']
                    datos_threat['scientific_name'] = request.POST['scientific_name']
                    datos_threat['typeThreat_id'] = request.POST['typeThreat_id']
                    datos_threat['active'] = False
                    datos_threat['wikipedia_link'] = "info wiki"
                    datos_threat['description'] = request.POST['scientific_name']
                    threat_cant = Threat.objects.filter().count()
                    datos_threat['code'] = threat_cant + 1
                    #agregar la amenaza inactiva porque un admin debe activarla

                    serializer = ThreatSerializer(data=datos_threat)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise AttributeError


            return Response({"success": ("GUARDA TODO")}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            pass
            return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)





##### DETECCION
##################################
# Agrega y modifica actividades de lote

@api_view(['POST', 'GET'])
def detection(request):
    if request.method == 'POST':
       try:
           with transaction.atomic():
               #print  request.POST['movil_id']

               datos_detection = {}
               datos_note = {}

               movil_id = request.POST['movil_id']


               datos_detection['user_id'] = request.user.id
               datos_detection['movil_id'] = movil_id
               datos_detection['date'] = request.POST['date']
               datos_detection['damage_level'] = request.POST['damage_level']
               datos_detection['threatDetail_id'] = request.POST['threat_id']

               datos_note['user_id'] = request.user.id
               datos_note['object_id'] = movil_id
               datos_note['object_type'] = "Detection"
               datos_note['content'] = request.POST['note']

	       import json
               actividades = request.POST['activity_id']
               actividades2 = actividades.replace("\\" ,"")
               actividades_json = json.loads(actividades2)

	       

               for registroActividad in actividades_json:

                    activity_id = registroActividad['id']
                    datos_detection['activity_id'] = activity_id
                    datos_detection['location_lat'] = registroActividad['location_lat']
                    datos_detection['location_long'] = registroActividad['location_long']
	            
	            existen = 0
                    if(activity_id == 0):
                        existen = Detection.objects.filter(movil_id=movil_id, location_lat=datos_detection['location_lat'] ,location_long=datos_detection['location_long']).count()
                    else:
                        existen = Detection.objects.filter(movil_id=movil_id,activity_id=activity_id).count()

                    if(existen == 0):
			
                    	serializer = DetectionSerializer(data=datos_detection)
                        if serializer.is_valid():
	                       	serializer.save()
				nota(datos_note)
			        image(request)
                                
                                sendPush.delay(datos_detection['threatDetail_id'])
                        else:
				raise AttributeError    
                    else:
			continue	     
               
           return Response({"success": (actividades_json)}, status=status.HTTP_200_OK)
           
       except (AttributeError, ObjectDoesNotExist):
              pass
              return Response({"error": (actividades_json)}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        detections = Detection.objects.filter()
        serializer = DetectionSerializer(detections, many=True)
        return JSONResponse(serializer.data)


def push(amenaza_id):
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
    #	idA = objectThreatDetail.threat_id
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
    #else:
	#dispositivos = Device.objects.filter(active=True)
        #for objectDevice in dispositivos:
        #	key_firebase = objectDevice.key_firebase
        #        title = "Envia a todos" + str(len(lista_usuarios_cultivos))
        #        body = str("1 Nueva detección en tu zona")
        #        resultado = push_notifications_view(key_firebase, title, body,data_message)   

def nota(datos_note):
    if(datos_note['content'] != ""):
    	object_id = datos_note['object_id']
    	existeNota = Note.objects.filter(object_id=object_id).count()
    	if (existeNota == 0):
        	serializerNote = NoteSerializer(data=datos_note)
        	if serializerNote.is_valid():
            		serializerNote.save()
        	else:
            		raise AttributeError
    


def image(request):
    request.POST['object_id'] = request.POST['movil_id']
    request.POST['object_type'] = "Detection"
    object_id = request.POST['movil_id']
    object_type = request.POST['object_type']
    #imagen = request.FILES['image']
    #print "aca"+imagen

    imagen = request.FILES.get('image', False)
    
    if(imagen):
    	existeImage = Picture.objects.filter(object_id=object_id, object_type=object_type).count()
    	if (existeImage == 0):
            serializer = PictureSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise AttributeError
    #else:
        # ACTUALIZO
        #picture = Picture.objects.filter(object_id=object_id, object_type=object_type)
        #for objectImage in picture:
                #serializer = PictureSerializer(objectImage, data=request.data)
                #if serializer.is_valid():
                #    serializer.save()
                #else:
                    #raise AttributeError


#detection-user
@api_view(['GET'])
def detectionUser(request):
    if request.method == 'GET':

        list_detection = []
        image_url = "sin imagen"
        note="sin comentario"
        va = 3
        list_activity = []

        detections = Detection.objects.filter(user_id=request.user.id)
        for objectDetection in detections:

            notes = Note.objects.filter(user_id=request.user.id, object_id=objectDetection.movil_id,object_type="Detection")
            for objectNote in notes:
                note = objectNote.content
            image_url = "sin imagen"
            picture = Picture.objects.filter(object_id=objectDetection.movil_id)
            for objectPicture in picture:
                image = str(objectPicture.image)
                image_url =  settings.MEDIA_URL + image


            activity_id = objectDetection.activity_id
            activites = Activity.objects.filter(user_id=request.user.id,movil_id=activity_id)
            for objectActivity in activites:
                activity_movil_id = objectActivity.movil_id
                dato_activity = {"activity_movil_id": activity_movil_id }
                list_activity.append(dato_activity)


            dato = {
                "movil_id": objectDetection.movil_id,
                "date": objectDetection.date,
                "threat_id": objectDetection.threatDetail_id,
                "note": note,
                "user_id": objectDetection.user_id,
                "image": image_url,
                "index_va":va,
                "activites": list_activity
            }
            list_activity = []
            list_detection.append(dato)

        return JSONResponse(list_detection)


@api_view(['GET'])
def detectionThreat(request,threat_id):
    if request.method == 'GET':

        list_detection = []
        image_url = "sin imagen"
        note = "sin comentario"
        sum_seen= 0
        sum_note = 0
        user = ""
        center_lat = 0
        center_long = 0

        detections = Detection.objects.filter(threatDetail_id=threat_id)
        for objectDetection in detections:
            usuario = UserModel.objects.filter(id=objectDetection.user_id)
            for objectUser in usuario:
                user = objectUser.username

            notes = Note.objects.filter(user_id=objectDetection.user_id, object_id=objectDetection.movil_id,object_type="Detection")
            for objectNote in notes:
                note = objectNote.content
            	sum_note = sum_note + 1
	    
	    if(objectDetection.activity_id != 0):
	    	activites = Activity.objects.filter(movil_id=objectDetection.activity_id)
            	for objectActivity in activites:
                	parcels = Parcel.objects.filter(movil_id=objectActivity.parcel_id)
                	for objectParcel in parcels:
                    		center_lat = objectParcel.center_lat
                    		center_long = objectParcel.center_long
	    else:
                center_lat = objectDetection.location_lat
                center_long = objectDetection.location_long

            picture = Picture.objects.filter(object_id=objectDetection.movil_id)
            for objectPicture in picture:
                image = str(objectPicture.image)
                if(image != ""):
                    image_url = settings.MEDIA_URL + image
                else:
                    image_url = "sin imagen"


            seens = Seen.objects.filter(object_id=objectDetection.movil_id,object_type="detection")
            for objectSeen in seens:
                sum_seen = sum_seen + 1



            dato = {
                    "movil_id": objectDetection.movil_id,
                    "date": objectDetection.date,
                    "damage_level": objectDetection.damage_level,
                    "threat_id": objectDetection.threatDetail_id,
                    "note": note,
                    "user": user,
                    "image": image_url,
                    "center_lat": center_lat,
                    "center_long": center_long,
                    "seen_sum": sum_seen,
                    "note_sum": sum_note
            }
            list_detection.append(dato)
            sum_note = 0
            sum_seen = 0

        return JSONResponse(list_detection)


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all().order_by()
    serializer_class = PictureSerializer

class NoteViewSet(viewsets.ModelViewSet):
        queryset = Note.objects.all().order_by()
        serializer_class = NoteSerializer

# return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)
#Vista agregar y modificar deteccion y detalle



##### VISTOS
##################################
# Agrega y modifica actividades de lote
@api_view(['POST', 'GET'])
def seen(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                for registro in request.data:
                    registro['user_id'] = request.user.id
                    #('user_id', 'object_id', 'object_type', 'date_time')
                    existeImage = Seen.objects.filter(object_id=registro['object_id'],object_type=registro['object_type'],user_id=registro['user_id']).count()
                    if (existeImage == 0):
                        serializer = SeenSerializer(data=registro)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise AttributeError
                    else:
                        continue
                        # ACTUALIZO
                        #detection = Detection.objects.filter(object_id=registro['object_id'],object_type=registro['object_type'],user_id=registro['user_id'])
                        #for objectNote in detection:
                            #serializer = DetectionSerializer(objectNote, data=registro)
                            #if serializer.is_valid():
                                #serializer.save()
                            #else:
                                #raise AttributeError

            return Response({"success": ("GUARDA TODO")}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            pass
            return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        seens = Seen.objects.filter()
        serializer = SeenSerializer(seens, many=True)
        return JSONResponse(serializer.data)


@api_view(['GET'])
def seenUser(request):
    if request.method == 'GET':
        seens = Seen.objects.filter(user_id=request.user.id)
        serializer = SeenSerializer(seens, many=True)
        return JSONResponse(serializer.data)


import calc_coor
@api_view(['GET'])
def detectionRadio(request, lat, long):
        if request.method == 'GET':
            #print lat
            #print long
            #seens = Seen.objects.filter(user_id=id)
            #serializer = SeenSerializer(seens, many=True)
            cantidad = calc_coor.cant_radio(lat,long)



            return JSONResponse(cantidad)
