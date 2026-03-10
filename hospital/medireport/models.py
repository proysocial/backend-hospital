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

# Al final de medireport/models.py (el de la raíz)

class ExamenSolicitud(models.Model):
    num_actmed = models.CharField(max_length=50, db_index=True)
    cod_examen = models.CharField(max_length=50, blank=True, null=True)
    desc_examen = models.CharField(max_length=255, blank=True, null=True)
    arealab = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    servicio = models.CharField(max_length=150, blank=True, null=True)
    dni_pac = models.CharField(max_length=20, blank=True, null=True)
    paciente = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(max_length=10, blank=True, null=True)
    fech_solic = models.DateField(blank=True, null=True, db_index=True)
    horsolic = models.CharField(max_length=10, blank=True, null=True)
    tipo_seguro = models.CharField(max_length=100, blank=True, null=True)
    dni_profesional = models.CharField(max_length=20, blank=True, null=True)
    profesional = models.CharField(max_length=255, blank=True, null=True)
    sede = models.CharField(max_length=100, blank=True, null=True)
    annos = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'examen_solicitud'

    def __str__(self):
        return f"{self.num_actmed} - {self.desc_examen}"


class ExamenResultado(models.Model):
    acto_medico = models.CharField(max_length=50, db_index=True)
    examen = models.CharField(max_length=50, blank=True, null=True)
    descexamen = models.CharField(max_length=255, blank=True, null=True)
    arealab = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    servicio = models.CharField(max_length=150, blank=True, null=True)
    dni = models.CharField(max_length=20, blank=True, null=True)
    paciente = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(max_length=10, blank=True, null=True)
    fecha_solicitud = models.DateField(blank=True, null=True)
    fecha_resultado = models.DateField(blank=True, null=True, db_index=True)
    resultado = models.CharField(max_length=50, blank=True, null=True)
    diagnostico = models.CharField(max_length=20, blank=True, null=True)
    des_diagn = models.CharField(max_length=255, blank=True, null=True)
    profesional = models.CharField(max_length=255, blank=True, null=True)
    informe_resultado = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'examen_resultado'

    def __str__(self):
        return f"{self.acto_medico} - {self.resultado}"