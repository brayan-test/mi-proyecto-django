from django.contrib import admin
from .models import Usuario,CicloAhorro,ParticipanteCiclo, Aporte, Pago
# Register your models here.
admin.site.register(Usuario)
admin.site.register(CicloAhorro)
admin.site.register(ParticipanteCiclo)
admin.site.register(Aporte)
admin.site.register(Pago)
