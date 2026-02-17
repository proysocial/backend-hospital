from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from ...models import RegistroTXT

class MetricsDashboardView(APIView):

    def get(self, request):

        data = {
            "examenes_mas_solicitados": list(
                RegistroTXT.objects.values("desc_examen")
                .annotate(total=Count("id"))
                .order_by("-total")[:10]
            ),

            "doctores_mas_atencion": list(
                RegistroTXT.objects.values("profesional")
                .annotate(total=Count("id"))
                .order_by("-total")[:10]
            ),

            "pacientes_por_enfermedad": list(
                RegistroTXT.objects.values("desc_examen")
                .annotate(total=Count("dni_paciente"))
            ),

            "pacientes_por_sexo": list(
                RegistroTXT.objects.values("sexo")
                .annotate(total=Count("id"))
            ),

            "servicios_mas_demanda": list(
                RegistroTXT.objects.values("servicio")
                .annotate(total=Count("id"))
                .order_by("-total")
            ),

            "tendencia_por_fecha": list(
                RegistroTXT.objects.values("fecha_solicitud")
                .annotate(total=Count("id"))
                .order_by("fecha_solicitud")
            ),

            "seguro_mas_usado": list(
                RegistroTXT.objects.values("tipo_seguro")
                .annotate(total=Count("id"))
            ),

            "area_laboratorio": list(
                RegistroTXT.objects.values("area_lab")
                .annotate(total=Count("id"))
            ),

            # INDICADORES GERENCIALES
            "carga_por_doctor": list(
                RegistroTXT.objects.values("profesional")
                .annotate(total=Count("id"))
            ),

            "ranking_enfermedades": list(
                RegistroTXT.objects.values("desc_examen")
                .annotate(total=Count("id"))
                .order_by("-total")
            ),

            "horas_pico": list(
                RegistroTXT.objects.values("hora_solicitud")
                .annotate(total=Count("id"))
                .order_by("-total")
            ),

            "pacientes_por_sede": list(
                RegistroTXT.objects.values("sede")
                .annotate(total=Count("id"))
            ),

            "distribucion_edad": list(
                RegistroTXT.objects.values("edad_anios")
                .annotate(total=Count("id"))
            )
        }

        return Response(data)