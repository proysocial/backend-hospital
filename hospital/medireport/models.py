from django.db import models

# Create your models here.
class RegistroTXT(models.Model):
    centro = models.CharField(max_length=10)
    periodo = models.CharField(max_length=10)

    tipo_examen = models.CharField(max_length=100)
    area_lab = models.CharField(max_length=100)
    servicio = models.CharField(max_length=150)

    dni_profesional = models.CharField(max_length=15)
    profesional = models.CharField(max_length=150)

    dni_paciente = models.CharField(max_length=15)
    paciente = models.CharField(max_length=150)
    sexo = models.CharField(max_length=1)

    cod_examen = models.CharField(max_length=20)
    desc_examen = models.TextField()

    fecha_solicitud = models.DateField(null=True)
    hora_solicitud = models.CharField(max_length=10, null=True)

    tipo_seguro = models.CharField(max_length=100)
    tipo_paciente = models.CharField(max_length=100)

    sede = models.CharField(max_length=100)

    edad_anios = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
