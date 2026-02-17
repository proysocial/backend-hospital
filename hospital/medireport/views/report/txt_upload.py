from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import RegistroTXT
import datetime

class UploadTXTView(APIView):

    def post(self, request):
        file = request.FILES['file']
        lines = file.read().decode("latin-1").splitlines()

        headers = lines[0].split("|")

        for line in lines[1:]:
            data = line.split("|")
            row = dict(zip(headers, data))

            RegistroTXT.objects.create(
                centro=row["CENTRO"],
                periodo=row["PERIODO"],
                tipo_examen=row["TIPEXAMEN"],
                area_lab=row["AREALAB"],
                servicio=row["SERVICIO"],

                dni_profesional=row["DNI_PROFESIONAL"],
                profesional=row["PROFESIONAL"],

                dni_paciente=row["DNI_PAC"],
                paciente=row["PACIENTE"],
                sexo=row["SEXO"],

                cod_examen=row["COD_EXAMEN"],
                desc_examen=row["DESC_EXAMEN"],

                fecha_solicitud=parse_fecha(row["FECH_SOLIC"]),
                hora_solicitud=row["HORSOLIC"],

                tipo_seguro=row["TIPO_SEGURO"],
                tipo_paciente=row["TIPO_PACIENTE"],

                sede=row["SEDE"],

                edad_anios=int(row["ANNOS"]) if row["ANNOS"] else None
            )

        return Response({"mensaje": "TXT procesado correctamente"})


def parse_fecha(valor):
    if valor:
        return datetime.datetime.strptime(valor, "%d/%m/%Y")
    return None