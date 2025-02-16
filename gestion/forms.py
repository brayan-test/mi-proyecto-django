from django import forms
from .models import CicloAhorro, Aporte, ParticipanteCiclo, Pago

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
        fields = ['usuario', 'ciclo']

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get("usuario")
        ciclo = cleaned_data.get("ciclo")

        # Verifica si el usuario ya está en el ciclo
        if ParticipanteCiclo.objects.filter(usuario=usuario, ciclo=ciclo).exists():
            raise forms.ValidationError(f"El usuario {usuario} ya está registrado en este ciclo.")

        return cleaned_data

class OrdenPagoForm(forms.ModelForm):
    class Meta:
        model = ParticipanteCiclo
        fields = ['orden_pago']

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['usuario', 'ciclo', 'monto']

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get("usuario")
        ciclo = cleaned_data.get("ciclo")

        # Validar que el usuario sea el siguiente en recibir pago
        participantes = ParticipanteCiclo.objects.filter(ciclo=ciclo).order_by('orden_pago')
        siguiente_participante = participantes.first()

        if siguiente_participante and siguiente_participante.usuario != usuario:
            raise forms.ValidationError("Este usuario no es el siguiente en recibir el pago.")

        return cleaned_data
