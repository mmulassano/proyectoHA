from django.contrib import admin



# Register your models here.
from .models import Threat,TypeThreat,Detection,Note,Picture,Seen,Detection

# Register your models here.
admin.site.register(TypeThreat)
admin.site.register(Threat)
admin.site.register(Picture)
admin.site.register(Note)
admin.site.register(Seen)
admin.site.register(Detection)

