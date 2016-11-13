from django.contrib import admin

from .models import Farm, Parcel, Activity,TypeCrop

# Register your models here.
admin.site.register(Farm)
admin.site.register(Parcel)
admin.site.register(Activity)
admin.site.register(TypeCrop)


