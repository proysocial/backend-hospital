from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from ...models import ReporteGuardado


# ─────────────────────────────────────────────────────────────────
# Helper: serializa un reporte como dict para las respuestas
# ─────────────────────────────────────────────────────────────────
def _serialize_reporte(reporte, include_datos=False):
    autor_info = None
    if reporte.autor:
        autor_info = {
            "id": reporte.autor.id,
            "nombre": reporte.autor.first_name,
            "apellido": reporte.autor.last_name,
            "correo": reporte.autor.email,
        }

    data = {
        "id": reporte.id,
        "nombre": reporte.nombre,
        "descripcion": reporte.descripcion,
        "autor": autor_info,
        "publicado": reporte.publicado,
        "fecha_creacion": reporte.fecha_creacion,
        "fecha_actualizacion": reporte.fecha_actualizacion,
    }
    if include_datos:
        data["datos"] = reporte.datos
    return data


# ─────────────────────────────────────────────────────────────────
# GET  /api/v1/reportes/                 → lista todos (admin/debug)
# POST /api/v1/reportes/                 → crea reporte (autenticado)
# ─────────────────────────────────────────────────────────────────
class ReporteGuardadoListCreateView(APIView):
    """
    GET:  Lista todos los reportes (solo metadata, sin datos pesados).
          Requiere autenticación.
    POST: Crea un nuevo reporte. El autor se toma del token JWT.
          Body: { nombre, descripcion?, datos }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reportes = ReporteGuardado.objects.select_related('autor').all()
        return Response([_serialize_reporte(r) for r in reportes], status=status.HTTP_200_OK)

    def post(self, request):
        nombre = request.data.get('nombre')
        datos = request.data.get('datos')
        descripcion = request.data.get('descripcion', '')

        if not nombre or not datos:
            return Response(
                {'error': 'Campos obligatorios: nombre, datos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reporte = ReporteGuardado.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            datos=datos,
            autor=request.user,
        )

        return Response(_serialize_reporte(reporte), status=status.HTTP_201_CREATED)


# ─────────────────────────────────────────────────────────────────
# GET    /api/v1/reportes/<pk>/          → detalle completo
# PUT    /api/v1/reportes/<pk>/          → editar (solo propietario)
# DELETE /api/v1/reportes/<pk>/          → eliminar (solo propietario)
# ─────────────────────────────────────────────────────────────────
class ReporteGuardadoDetailView(APIView):
    """
    GET:    Devuelve el reporte completo (datos incluidos).
    PUT:    Edita nombre, descripcion o datos del reporte.
            Solo el propietario puede editar.
    DELETE: Elimina el reporte.
            Solo el propietario puede eliminar.
    """
    permission_classes = [IsAuthenticated]

    def _get_reporte(self, pk):
        try:
            return ReporteGuardado.objects.select_related('autor').get(pk=pk)
        except ReporteGuardado.DoesNotExist:
            return None

    def get(self, request, pk):
        reporte = self._get_reporte(pk)
        if not reporte:
            return Response({'error': 'Reporte no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Solo el propietario o si está publicado
        if not reporte.publicado and reporte.autor != request.user:
            return Response({'error': 'No tienes permiso para ver este reporte'}, status=status.HTTP_403_FORBIDDEN)

        return Response(_serialize_reporte(reporte, include_datos=True), status=status.HTTP_200_OK)

    def put(self, request, pk):
        reporte = self._get_reporte(pk)
        if not reporte:
            return Response({'error': 'Reporte no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if reporte.autor != request.user:
            return Response({'error': 'Solo el propietario puede editar este reporte'}, status=status.HTTP_403_FORBIDDEN)

        reporte.nombre = request.data.get('nombre', reporte.nombre)
        reporte.descripcion = request.data.get('descripcion', reporte.descripcion)
        if 'datos' in request.data:
            reporte.datos = request.data.get('datos')
        reporte.save()

        return Response({
            **_serialize_reporte(reporte),
            'mensaje': 'Reporte actualizado correctamente'
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        reporte = self._get_reporte(pk)
        if not reporte:
            return Response({'error': 'Reporte no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if reporte.autor != request.user:
            return Response({'error': 'Solo el propietario puede eliminar este reporte'}, status=status.HTTP_403_FORBIDDEN)

        reporte.delete()
        return Response({'mensaje': 'Reporte eliminado exitosamente'}, status=status.HTTP_200_OK)


# ─────────────────────────────────────────────────────────────────
# GET /api/v1/reportes/mis-reportes/     → reportes del usuario autenticado
# ─────────────────────────────────────────────────────────────────
class MisReportesView(APIView):
    """
    GET: Devuelve SOLO los reportes del usuario autenticado (públicos y privados).
         El usuario únicamente ve sus propios reportes.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reportes = ReporteGuardado.objects.filter(autor=request.user).select_related('autor')
        return Response([_serialize_reporte(r) for r in reportes], status=status.HTTP_200_OK)


# ─────────────────────────────────────────────────────────────────
# PATCH /api/v1/reportes/<pk>/publicar/  → publica/despublica reporte
# ─────────────────────────────────────────────────────────────────
class PublicarReporteView(APIView):
    """
    PATCH: Cambia el estado 'publicado' de un reporte.
           Solo el propietario puede publicar/despublicar.
           Body opcional: { publicado: true|false }  (por defecto toggle)
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            reporte = ReporteGuardado.objects.select_related('autor').get(pk=pk)
        except ReporteGuardado.DoesNotExist:
            return Response({'error': 'Reporte no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if reporte.autor != request.user:
            return Response({'error': 'Solo el propietario puede publicar este reporte'}, status=status.HTTP_403_FORBIDDEN)

        # Si se pasa explícito, usarlo; si no, hacer toggle
        if 'publicado' in request.data:
            reporte.publicado = bool(request.data.get('publicado'))
        else:
            reporte.publicado = not reporte.publicado

        reporte.save()
        estado = 'publicado' if reporte.publicado else 'despublicado'
        return Response({
            'id': reporte.id,
            'publicado': reporte.publicado,
            'mensaje': f'Reporte {estado} exitosamente'
        }, status=status.HTTP_200_OK)


# ─────────────────────────────────────────────────────────────────
# GET /api/v1/reportes/publicos/         → reportes publicados (todos pueden ver)
# ─────────────────────────────────────────────────────────────────
class ReportesPublicosView(APIView):
    """
    GET: Devuelve todos los reportes marcados como publicados.
         No requiere autenticación — cualquiera puede verlos.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        reportes = ReporteGuardado.objects.filter(publicado=True).select_related('autor')
        return Response([_serialize_reporte(r) for r in reportes], status=status.HTTP_200_OK)


# ─────────────────────────────────────────────────────────────────
# GET /api/v1/reportes/publicos/<pk>/    → detalle de reporte público
# ─────────────────────────────────────────────────────────────────
class ReportePublicoDetalleView(APIView):
    """
    GET: Devuelve el detalle completo de un reporte público (datos incluidos).
         No requiere autenticación.
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            reporte = ReporteGuardado.objects.select_related('autor').get(pk=pk, publicado=True)
        except ReporteGuardado.DoesNotExist:
            return Response({'error': 'Reporte no encontrado o no está publicado'}, status=status.HTTP_404_NOT_FOUND)

        return Response(_serialize_reporte(reporte, include_datos=True), status=status.HTTP_200_OK)
