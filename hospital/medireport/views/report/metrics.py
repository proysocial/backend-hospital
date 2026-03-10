from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg, F, Q, ExpressionWrapper, DurationField
from django.db.models.functions import TruncMonth, TruncHour, ExtractHour
from ...models import ExamenSolicitud, ExamenResultado


class MetricsDashboardView(APIView):
    """
    Endpoint principal de métricas para el dashboard.

    Parámetros opcionales:
    - area: filtrar por AREALAB
    - servicio: filtrar por SERVICIO
    - fecha_inicio: YYYY-MM-DD
    - fecha_fin: YYYY-MM-DD
    """

    def get(self, request):
        # Filtros opcionales
        area = request.query_params.get('area', None)
        servicio = request.query_params.get('servicio', None)
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)

        # QuerySets base con filtros
        qs_solic = ExamenSolicitud.objects.all()
        qs_result = ExamenResultado.objects.all()

        if area:
            # Los tabs ahora usan SERVICIO como clave (no AREALAB)
            qs_solic = qs_solic.filter(servicio__icontains=area)
            qs_result = qs_result.filter(servicio__icontains=area)

        if servicio:
            qs_solic = qs_solic.filter(servicio__icontains=servicio)
            qs_result = qs_result.filter(servicio__icontains=servicio)

        if fecha_inicio:
            qs_solic = qs_solic.filter(fech_solic__gte=fecha_inicio)
            qs_result = qs_result.filter(fecha_solicitud__gte=fecha_inicio)

        if fecha_fin:
            qs_solic = qs_solic.filter(fech_solic__lte=fecha_fin)
            qs_result = qs_result.filter(fecha_solicitud__lte=fecha_fin)

        # ─── KPIs globales ───────────────────────────────────────────────────
        total_solicitados = qs_solic.count()
        total_con_resultado = qs_result.count()
        tasa_resultado = round(
            (total_con_resultado / total_solicitados * 100) if total_solicitados > 0 else 0, 1
        )

        # ─── Pacientes por sexo ──────────────────────────────────────────────
        pacientes_sexo = list(
            qs_solic.exclude(sexo__isnull=True).exclude(sexo='')
            .values('sexo')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # ─── Exámenes más solicitados ────────────────────────────────────────
        examenes_mas_solicitados = list(
            qs_solic.exclude(desc_examen__isnull=True)
            .values('desc_examen', 'cod_examen')
            .annotate(total=Count('id'))
            .order_by('-total')[:10]
        )

        # ─── Servicios más demandados ────────────────────────────────────────
        servicios_demanda = list(
            qs_solic.exclude(servicio__isnull=True)
            .values('servicio')
            .annotate(total=Count('id'))
            .order_by('-total')[:10]
        )

        # ─── Tendencia mensual ───────────────────────────────────────────────
        tendencia = list(
            qs_solic.filter(fech_solic__isnull=False)
            .annotate(mes=TruncMonth('fech_solic'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
        )
        tendencia_fmt = [
            {'mes': t['mes'].strftime('%Y-%m') if t['mes'] else None, 'total': t['total']}
            for t in tendencia
        ]

        # ─── Horas pico ─────────────────────────────────────────────────────
        horas_pico = list(
            qs_solic.exclude(horsolic__isnull=True).exclude(horsolic='')
            .values('horsolic')
            .annotate(total=Count('id'))
            .order_by('-total')[:10]
        )

        # ─── Distribución por edad ───────────────────────────────────────────
        def rango_edad(qs):
            rangos = [
                ('0-10', 0, 10), ('11-20', 11, 20), ('21-30', 21, 30),
                ('31-40', 31, 40), ('41-50', 41, 50), ('51-60', 51, 60),
                ('61-70', 61, 70), ('71+', 71, 999),
            ]
            result = []
            for label, min_a, max_a in rangos:
                count = qs.filter(annos__gte=min_a, annos__lte=max_a).count()
                if count > 0:
                    result.append({'rango': label, 'total': count})
            return result

        distribucion_edad = rango_edad(qs_solic)

        # ─── Tipo de seguro ──────────────────────────────────────────────────
        seguro_uso = list(
            qs_solic.exclude(tipo_seguro__isnull=True).exclude(tipo_seguro='')
            .values('tipo_seguro')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # ─── Doctores con más atenciones ─────────────────────────────────────
        doctores = list(
            qs_solic.exclude(profesional__isnull=True).exclude(profesional='')
            .values('profesional')
            .annotate(total=Count('id'))
            .order_by('-total')[:10]
        )

        # ─── Sedes ───────────────────────────────────────────────────────────
        sedes = list(
            qs_solic.exclude(sede__isnull=True).exclude(sede='')
            .values('sede')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # ─── NORMAL vs PATOLOGICO por área ───────────────────────────────────
        normal_patologico = list(
            qs_result.exclude(resultado__isnull=True).exclude(resultado='')
            .values('resultado', 'arealab')
            .annotate(total=Count('id'))
            .order_by('arealab', 'resultado')
        )

        # Simplificado: solo global
        normal_patologico_global = list(
            qs_result.exclude(resultado__isnull=True).exclude(resultado='')
            .values('resultado')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # ─── Diagnósticos CIE-10 más frecuentes ─────────────────────────────
        diagnosticos_cie10 = list(
            qs_result.exclude(diagnostico__isnull=True).exclude(diagnostico='')
            .exclude(diagnostico='0')
            .values('diagnostico', 'des_diagn')
            .annotate(total=Count('id'))
            .order_by('-total')[:15]
        )

        # ─── SERVICIOS para los TABS (siempre todos, sin filtro de área/fecha) ─
        # Se usa ExamenSolicitud base para que los tabs nunca desaparezcan
        servicios_raw = list(
            ExamenSolicitud.objects.exclude(servicio__isnull=True).exclude(servicio='')
            .values('servicio')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        # Reutilizamos clave 'arealab' para no romper el frontend existente
        areas = [{'arealab': s['servicio'], 'total': s['total']} for s in servicios_raw]

        # ─── RESUMEN POR SERVICIO (para las tabs del dashboard) ──────────────
        resumen_areas = {}
        for a in areas:
            nombre_servicio = a['arealab']  # contiene valor de SERVICIO

            # Base con filtros de fecha aplicados también al detalle
            qs_s = ExamenSolicitud.objects.filter(servicio=nombre_servicio)
            qs_r = ExamenResultado.objects.filter(servicio=nombre_servicio)
            if fecha_inicio:
                qs_s = qs_s.filter(fech_solic__gte=fecha_inicio)
                qs_r = qs_r.filter(fecha_solicitud__gte=fecha_inicio)
            if fecha_fin:
                qs_s = qs_s.filter(fech_solic__lte=fecha_fin)
                qs_r = qs_r.filter(fecha_solicitud__lte=fecha_fin)

            # Top exámenes del servicio
            top_examenes = list(
                qs_s.exclude(desc_examen__isnull=True)
                .values('desc_examen')
                .annotate(total=Count('id'))
                .order_by('-total')[:8]
            )

            # Áreas de laboratorio que atienden este servicio
            areas_servicio = list(
                qs_s.exclude(arealab__isnull=True).exclude(arealab='')
                .values('arealab')
                .annotate(total=Count('id'))
                .order_by('-total')[:8]
            )
            # Renombrar para compatibilidad con el frontend
            for item in areas_servicio:
                item['servicio'] = item.pop('arealab')

            # Normal vs Patológico
            resultado_dist = list(
                qs_r.exclude(resultado__isnull=True).exclude(resultado='')
                .values('resultado')
                .annotate(total=Count('id'))
            )

            # CIE-10 del servicio
            cie10_serv = list(
                qs_r.exclude(diagnostico__isnull=True).exclude(diagnostico='').exclude(diagnostico='0')
                .values('diagnostico', 'des_diagn')
                .annotate(total=Count('id'))
                .order_by('-total')[:10]
            )

            # Tendencia del servicio
            tend_serv = list(
                qs_s.filter(fech_solic__isnull=False)
                .annotate(mes=TruncMonth('fech_solic'))
                .values('mes')
                .annotate(total=Count('id'))
                .order_by('mes')
            )
            tend_serv_fmt = [
                {'mes': t['mes'].strftime('%Y-%m'), 'total': t['total']}
                for t in tend_serv if t['mes']
            ]

            # Sexo del servicio
            sexo_serv = list(
                qs_s.exclude(sexo__isnull=True).exclude(sexo='')
                .values('sexo')
                .annotate(total=Count('id'))
            )

            # Doctores que más solicitan en este servicio
            doctores_serv = list(
                qs_s.exclude(profesional__isnull=True).exclude(profesional='')
                .values('profesional')
                .annotate(total=Count('id'))
                .order_by('-total')[:8]
            )

            resumen_areas[nombre_servicio] = {
                'total_solicitados': qs_s.count(),
                'total_con_resultado': qs_r.count(),
                'top_examenes': top_examenes,
                'servicios': areas_servicio,  # aquí son las ÁREAS de lab que atienden
                'resultado_distribucion': resultado_dist,
                'cie10': cie10_serv,
                'tendencia': tend_serv_fmt,
                'sexo': sexo_serv,
                'doctores': doctores_serv,
            }

        # ─── Examen más solicitado (para KPI) ───────────────────────────────
        examen_top = examenes_mas_solicitados[0]['desc_examen'] if examenes_mas_solicitados else 'N/A'

        return Response({
            # KPIs
            'kpis': {
                'total_solicitados': total_solicitados,
                'total_con_resultado': total_con_resultado,
                'tasa_resultado': tasa_resultado,
                'examen_top': examen_top,
                'total_femenino': next((x['total'] for x in pacientes_sexo if x['sexo'] in ['F', 'FEMENINO']), 0),
                'total_masculino': next((x['total'] for x in pacientes_sexo if x['sexo'] in ['M', 'MASCULINO']), 0),
            },
            # Métricas globales
            'examenes_mas_solicitados': examenes_mas_solicitados,
            'servicios_mas_demanda': servicios_demanda,
            'tendencia_mensual': tendencia_fmt,
            'horas_pico': horas_pico,
            'distribucion_edad': distribucion_edad,
            'seguro_uso': seguro_uso,
            'doctores_top': doctores,
            'sedes': sedes,
            'pacientes_por_sexo': pacientes_sexo,
            'normal_patologico': normal_patologico_global,
            'diagnosticos_cie10': diagnosticos_cie10,
            'areas': areas,
            # Métricas por área (para tabs)
            'resumen_por_area': resumen_areas,
        })


class AreasListView(APIView):
    """
    Retorna la lista de áreas disponibles.
    GET /api/areas/
    """
    def get(self, request):
        areas = list(
            ExamenSolicitud.objects.exclude(arealab__isnull=True).exclude(arealab='')
            .values('arealab')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        return Response({'areas': areas})


class AreaDetalleView(APIView):
    """
    Detalle drill-down de un área específica.
    GET /api/area-detalle/?area=RADIOLOGIA DIAGNOSTICA&servicio=RX TORAX
    """
    def get(self, request):
        area = request.query_params.get('area')
        servicio = request.query_params.get('servicio', None)

        if not area:
            return Response({'error': 'Parámetro "area" requerido'}, status=400)

        qs_s = ExamenSolicitud.objects.filter(arealab__icontains=area)
        qs_r = ExamenResultado.objects.filter(arealab__icontains=area)

        if servicio:
            qs_s = qs_s.filter(servicio__icontains=servicio)
            qs_r = qs_r.filter(servicio__icontains=servicio)

        # Servicios dentro del área
        servicios = list(
            qs_s.exclude(servicio__isnull=True).exclude(servicio='')
            .values('servicio')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # Exámenes dentro del área/servicio
        examenes = list(
            qs_s.exclude(desc_examen__isnull=True)
            .values('cod_examen', 'desc_examen')
            .annotate(total=Count('id'))
            .order_by('-total')[:15]
        )

        # CIE-10
        cie10 = list(
            qs_r.exclude(diagnostico__isnull=True).exclude(diagnostico='').exclude(diagnostico='0')
            .values('diagnostico', 'des_diagn')
            .annotate(total=Count('id'))
            .order_by('-total')[:10]
        )

        # Resultado
        resultado_dist = list(
            qs_r.exclude(resultado__isnull=True).exclude(resultado='')
            .values('resultado')
            .annotate(total=Count('id'))
        )

        # Tendencia
        tendencia = list(
            qs_s.filter(fech_solic__isnull=False)
            .annotate(mes=TruncMonth('fech_solic'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
        )

        return Response({
            'area': area,
            'servicio_filtro': servicio,
            'total_solicitados': qs_s.count(),
            'total_con_resultado': qs_r.count(),
            'servicios': servicios,
            'examenes': examenes,
            'cie10': cie10,
            'resultado_distribucion': resultado_dist,
            'tendencia': [
                {'mes': t['mes'].strftime('%Y-%m'), 'total': t['total']}
                for t in tendencia if t['mes']
            ],
        })