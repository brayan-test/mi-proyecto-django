from django.db import models
from django.contrib.auth.models import AbstractUser
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
    ciclo = models.ForeignKey(CicloAhorro, on_delete=models.CASCADE)
    fecha_registro = models.DateField(auto_now_add=True)
    orden_pago = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} en {self.ciclo.nombre}"
    
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

    monto = models.DecimalField(max_digits=10,decimal_places=2)
    fecha_pago = models.DateField(auto_now_add=True)
    # Agregar lógica para pagar al participante, al realizar este pago cambiará el periodo

    def __str__(self):
        return f"Pago a {self.usuario.username} de Bs{self.monto}"






