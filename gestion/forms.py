from django import forms
from .models import CicloAhorro, Aporte

class CicloAhorroForm(forms.ModelForm):
    class Meta:
        model = CicloAhorro
        fields = ['nombre','fecha_inicio','fecha_fin','monto_total']

class AporteForm(forms.ModelForm):
    class Meta:
        model = Aporte
        fields = ['usuario','ciclo','monto']

