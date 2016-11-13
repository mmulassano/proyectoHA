import math
from models import Detection
from mapeo.models import Activity, Parcel

def calc_distancia(lat1, long1, lat2, long2):
    distancia = 0
    rad=math.pi * 180
    dlat = lat2 - lat1
    dlong = long2 - long1
    #radio de la tierra km
    R= 6372.795477598
    a=(math.sin(rad*dlat/2))**2 + math.cos(rad*lat1) * math.cos(rad*lat2) * (math.sin(rad*dlong/2))**2
    distancia = 2 * R * math.asin(math.sqrt(a))

    return distancia


#Cantidad de detecciones en un radio de 100km
def cant_radio(lat,long):
    cantidad = 0
    distancias = []
    #busco todas las detecciones
    detections = Detection.objects.filter()

    for objectDetection in detections:
        activity_id = objectDetection.activity_id
        activites = Activity.objects.filter(movil_id=activity_id)
        for objectActivity in activites:
            parcel_id = objectActivity.parcel_id
            parcels = Parcel.objects.filter(movil_id=parcel_id)
            for objectParcel in parcels:
                parcel_center_lat = objectParcel.center_lat
                parcel_center_long = objectParcel.center_long

                #distancia = calc_distancia(lat,long,parcel_center_lat,parcel_center_long)
                #distancias.append(distancia)

    #print distancias
    cantidad = detections.count()


    return cantidad