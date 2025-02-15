from django import forms
from .models import CicloAhorro, Aporte, ParticipanteCiclo

class CicloAhorroForm(forms.ModelForm):
    class Meta:
        model = CicloAhorro
        fields = ['nombre','fecha_inicio','fecha_fin','monto_por_participante','periodo']

class AporteForm(forms.ModelForm):
    class Meta:
        model = Aporte
        fields = ['usuario','ciclo']

class ParticipanteCicloForm(forms.ModelForm):
    class Meta:
        model = ParticipanteCiclo
        fields = ['usuario','ciclo']