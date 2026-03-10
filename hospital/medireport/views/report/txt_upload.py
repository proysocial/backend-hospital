import io
import csv
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import ExamenSolicitud, ExamenResultado


def parse_fecha(valor):
    """Convierte string de fecha a objeto date"""
    if not valor or valor.strip() == '':
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(valor.strip(), fmt).date()
        except ValueError:
            continue
    return None


def detectar_tipo_txt(columnas):
    """
    Detecta automáticamente si es solicitudes o resultados
    basado en los nombres de columnas
    """
    columnas_set = set(c.upper().strip() for c in columnas)
    
    # Columnas exclusivas de solicitudes
    if 'NUM_ACTMED' in columnas_set or 'HORSOLIC' in columnas_set:
        return 'solicitudes'
    
    # Columnas exclusivas de resultados
    if 'ACTO_MEDICO' in columnas_set or 'RESULTADO' in columnas_set or 'DIAGNOSTICO' in columnas_set:
        return 'resultados'
    
    return 'desconocido'


def procesar_solicitudes(filas, delimiter='|'):
    """Procesa filas del TXT de solicitudes"""
    creados = 0
    errores = 0
    
    ExamenSolicitud.objects.all().delete()
    
    for fila in filas:
        num = fila.get('NUM_ACTMED', '').strip()
        if num in ('', 'TOTAL', 'NUM_ACTMED'):
            continue
        try:
            ExamenSolicitud.objects.create(
                num_actmed=num,
                cod_examen=fila.get('COD_EXAMEN', '').strip() or None,
                desc_examen=fila.get('DESC_EXAMEN', '').strip() or None,
                arealab=fila.get('AREALAB', '').strip() or None,
                servicio=fila.get('SERVICIO', '').strip() or None,
                dni_pac=fila.get('DNI_PAC', '').strip() or None,
                paciente=fila.get('PACIENTE', '').strip() or None,
                sexo=fila.get('SEXO', '').strip() or None,
                fech_solic=parse_fecha(fila.get('FECH_SOLIC', '')),
                horsolic=fila.get('HORSOLIC', '').strip() or None,
                tipo_seguro=fila.get('TIPO_SEGURO', '').strip() or None,
                dni_profesional=fila.get('DNI_PROFESIONAL', '').strip() or None,
                profesional=fila.get('PROFESIONAL', '').strip() or None,
                sede=fila.get('SEDE', '').strip() or None,
                annos=int(fila.get('ANNOS', 0)) if fila.get('ANNOS', '').strip().isdigit() else None,
            )
            creados += 1
        except Exception:
            errores += 1
    
    return creados, errores


def procesar_resultados(filas):
    """Procesa filas del TXT de resultados"""
    creados = 0
    errores = 0
    
    ExamenResultado.objects.all().delete()
    
    for fila in filas:
        acto = fila.get('ACTO_MEDICO', '').strip()
        if acto in ('', 'TOTAL', 'ACTO_MEDICO'):
            continue
        try:
            ExamenResultado.objects.create(
                acto_medico=acto,
                examen=fila.get('EXAMEN', '').strip() or None,
                descexamen=fila.get('DESCEXAMEN', '').strip() or None,
                arealab=fila.get('AREALAB', '').strip() or None,
                servicio=fila.get('SERVICIO', '').strip() or None,
                dni=fila.get('DNI', '').strip() or None,
                paciente=fila.get('PACIENTE', '').strip() or None,
                sexo=fila.get('SEXO', '').strip() or None,
                fecha_solicitud=parse_fecha(fila.get('FECHA_SOLICITUD', '')),
                fecha_resultado=parse_fecha(fila.get('FECHA_RESULTADO', '')),
                resultado=fila.get('RESULTADO', '').strip() or None,
                diagnostico=fila.get('DIAGNOSTICO', '').strip() or None,
                des_diagn=fila.get('DES_DIAGN', '').strip() or None,
                profesional=fila.get('PROFESIONAL', '').strip() or None,
                informe_resultado=fila.get('INFORME_RESULTADO', '').strip() or None,
            )
            creados += 1
        except Exception:
            errores += 1
    
    return creados, errores


class UploadTXTView(APIView):
    """
    Endpoint para subir los dos archivos TXT.
    Detecta automáticamente qué tipo es cada uno.
    POST /api/upload-txt/
    Body: multipart/form-data con campo 'files' 
    """

    def post(self, request):
        archivos = request.FILES.getlist('files')
        
        if not archivos:
            # Intentar con campo individual
            archivo1 = request.FILES.get('file1')
            archivo2 = request.FILES.get('file2')
            if archivo1:
                archivos.append(archivo1)
            if archivo2:
                archivos.append(archivo2)
        
        if not archivos:
            return Response(
                {'error': 'No se enviaron archivos. Use campo "files" o "file1"/"file2".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resultados = []
        
        for archivo in archivos:
            try:
                contenido = archivo.read().decode('latin-1')
                reader = csv.DictReader(io.StringIO(contenido), delimiter='|')
                filas = list(reader)
                
                if not filas:
                    resultados.append({
                        'archivo': archivo.name,
                        'error': 'Archivo vacío o sin datos'
                    })
                    continue
                
                tipo = detectar_tipo_txt(filas[0].keys())
                
                if tipo == 'solicitudes':
                    creados, errores = procesar_solicitudes(filas)
                    resultados.append({
                        'archivo': archivo.name,
                        'tipo': 'solicitudes',
                        'registros_creados': creados,
                        'errores': errores
                    })
                elif tipo == 'resultados':
                    creados, errores = procesar_resultados(filas)
                    resultados.append({
                        'archivo': archivo.name,
                        'tipo': 'resultados',
                        'registros_creados': creados,
                        'errores': errores
                    })
                else:
                    resultados.append({
                        'archivo': archivo.name,
                        'error': 'No se pudo detectar el tipo de archivo. Verificar columnas.'
                    })
                    
            except Exception as e:
                resultados.append({
                    'archivo': archivo.name,
                    'error': str(e)
                })
        
        return Response({
            'message': 'Procesamiento completado',
            'resultados': resultados
        }, status=status.HTTP_200_OK)