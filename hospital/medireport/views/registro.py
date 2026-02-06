from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def registrar_usuario(request):
    correo = request.data.get('correo')
    contrasena = request.data.get('contrasena')
    nombre = request.data.get('nombre', '')
    apellido = request.data.get('apellido', '')

    if not correo or not contrasena:
        return Response(
            {"error": "Correo y contraseña son obligatorios"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validar correo único
    if User.objects.filter(email=correo).exists():
        return Response(
            {"error": "El correo ya está registrado"},
            status=status.HTTP_409_CONFLICT
        )

    # Usamos el correo como username 
    usuario = User.objects.create_user(
        username=correo,
        email=correo,
        password=contrasena,   
        first_name=nombre,
        last_name=apellido
    )

    return Response(
        {
            "mensaje": "Usuario registrado correctamente",
            "usuario": {
                "id": usuario.id,
                "correo": usuario.email,
                "nombre": usuario.first_name,
                "apellido": usuario.last_name
            }
        },
        status=status.HTTP_201_CREATED
    )
