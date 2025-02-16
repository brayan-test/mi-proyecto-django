from django.db import models
from django.contrib.auth.models import AbstractUser
from random import shuffle
# Create your models here.

# Modelo para crear un USUARIO con roles
class Usuario(AbstractUser):
    ROLES = [('ADMIN','Administrador'), ('PARTICIPANTE','Participante')]

    rol = models.CharField(max_length=15,choices=ROLES,default='PARTICIPANTE')

    def __str__(self):
        return self.username
    
class CicloAhorro(models.Model):
    PERIODOS = [('SEMANAL',"Semanal"),('MENSUAL',"Mensual"),('ANUAL',"Anual")]
    ESTADOS = [('PENDIENTE','pendiente'),('EN PROCESO','En Proceso'),('FINALIZADO','Finalizado')]

    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto_por_participante = models.DecimalField(max_digits=10,decimal_places=2)
    periodo = models.CharField(max_length=10, choices = PERIODOS, default='MENSUAL')
    estado = models.CharField(max_length=15, choices = ESTADOS, default='PENDIENTE')
    
    def __str__(self):
        return self.nombre

# Modelo intermedio para relacionar USUARIOS a CICLOAHORRO
class ParticipanteCiclo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(CicloAhorro, on_delete=models.CASCADE, related_name="participantes")
    fecha_registro = models.DateField(auto_now_add=True)
    orden_pago = models.IntegerField(null=True, blank=True)  # Para definir el orden de pagos

    def __str__(self):
        return f"{self.usuario.username} en {self.ciclo.nombre} (Orden: {self.orden_pago})"

    @classmethod
    def sortear_orden(cls, ciclo_id):
        """Sortea el orden de pago entre los participantes del ciclo"""
        participantes = list(cls.objects.filter(ciclo_id=ciclo_id))
        shuffle(participantes)  # Mezcla aleatoriamente los participantes
        for index, participante in enumerate(participantes, start=1):
            participante.orden_pago = index
            participante.save()
    
class Aporte(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(CicloAhorro, on_delete=models.CASCADE)

    monto = models.DecimalField(max_digits=10,decimal_places=2)
    fecha_aporte = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Aporte de {self.usuario.username} - Bs{self.monto}"
    

class Pago(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(CicloAhorro, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Verifica que el pago siga el orden de pago definido en el ciclo"""
        participantes = ParticipanteCiclo.objects.filter(ciclo=self.ciclo).order_by('orden_pago')
        siguiente_participante = participantes.first()  # El primero en la lista debe recibir el pago

        if siguiente_participante.usuario != self.usuario:
            raise ValueError("No puedes pagar a este usuario aún. Respeta el orden de pago.")

        # Eliminar al participante que ya recibió el pago
        siguiente_participante.delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pago a {self.usuario.username} de Bs{self.monto} en {self.ciclo.nombre}"







