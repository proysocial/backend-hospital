from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def login_por_correo(request):
    correo = request.data.get('correo')
    contrasena = request.data.get('contrasena')

    if not correo or not contrasena:
        return Response(
            {"error": "Correo y contraseña son obligatorios"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        usuario = User.objects.get(email=correo)
    except User.DoesNotExist:
        return Response(
            {"error": "Correo o contraseña incorrectos"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    usuario_autenticado = authenticate(
        username=usuario.username,
        password=contrasena
    )

    if usuario_autenticado is None:
        return Response(
            {"error": "Correo o contraseña incorrectos"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not usuario_autenticado.is_active:
        return Response(
            {"error": "Usuario inactivo"},
            status=status.HTTP_403_FORBIDDEN
        )

    refresh = RefreshToken.for_user(usuario_autenticado)

    return Response({
        "mensaje": "Login exitoso",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "usuario": {
            "id": usuario.id,
            "correo": usuario.email,
            "nombre": usuario.first_name,
            "apellido": usuario.last_name
        }
    })
