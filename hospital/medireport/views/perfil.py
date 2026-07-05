from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class EditarPerfilView(APIView):
    """
    GET:  Devuelve los datos del perfil del usuario autenticado.
    PUT:  Edita nombre, apellido o correo del usuario autenticado.
          Body: { nombre?, apellido?, correo? }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            "id": u.id,
            "nombre": u.first_name,
            "apellido": u.last_name,
            "correo": u.email,
            "username": u.username,
            "fecha_registro": u.date_joined,
        })

    def put(self, request):
        u = request.user

        nombre = request.data.get('nombre', u.first_name)
        apellido = request.data.get('apellido', u.last_name)
        correo = request.data.get('correo', u.email)

        # Validar que el correo no esté en uso por otro usuario
        if correo != u.email and User.objects.filter(email=correo).exclude(pk=u.pk).exists():
            return Response(
                {'error': 'El correo ya está en uso por otro usuario'},
                status=status.HTTP_409_CONFLICT
            )

        u.first_name = nombre
        u.last_name = apellido
        u.email = correo
        # Si el username era el correo anterior, actualizarlo también
        if u.username == u.email or u.username == request.data.get('correo_anterior', ''):
            u.username = correo
        u.save()

        return Response({
            "mensaje": "Perfil actualizado correctamente",
            "usuario": {
                "id": u.id,
                "nombre": u.first_name,
                "apellido": u.last_name,
                "correo": u.email,
            }
        })


class CambiarContrasenaDirectaView(APIView):
    """
    POST: Cambia la contraseña del usuario autenticado directamente.
          Solo requiere la nueva contraseña (no pide la anterior ni código).
          Body: { nueva_contrasena }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nueva = request.data.get('nueva_contrasena')

        if not nueva:
            return Response(
                {'error': 'El campo nueva_contrasena es obligatorio'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(nueva) < 6:
            return Response(
                {'error': 'La contraseña debe tener al menos 6 caracteres'},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.set_password(nueva)
        request.user.save()

        return Response({'mensaje': 'Contraseña actualizada correctamente'})
