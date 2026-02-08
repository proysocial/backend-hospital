import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def enviar_codigo_recuperacion(request):
    correo = request.data.get('correo')

    if not correo:
        return Response(
            {"error": "El correo es obligatorio"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        User.objects.get(email=correo)
    except User.DoesNotExist:
        return Response(
            {"error": "Correo no registrado"},
            status=status.HTTP_404_NOT_FOUND
        )

    codigo = str(random.randint(100000, 999999))

    cache.set(f"recuperacion_{correo}", codigo, timeout=300)

    send_mail(
        subject="Recuperación de contraseña",
        message=f"Tu código de recuperación es: {codigo}",
        from_email="proysocialperu@gmail.com",
        recipient_list=[correo],
    )

    return Response({"mensaje": "Código enviado al correo"})


@api_view(['POST'])
def cambiar_contrasena(request):
    correo = request.data.get('correo')
    codigo = request.data.get('codigo')
    nueva_contrasena = request.data.get('nueva_contrasena')

    if not correo or not codigo or not nueva_contrasena:
        return Response(
            {"error": "Faltan datos"},
            status=status.HTTP_400_BAD_REQUEST
        )

    codigo_guardado = cache.get(f"recuperacion_{correo}")

    if codigo_guardado is None:
        return Response(
            {"error": "El código expiró"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if codigo_guardado != codigo:
        return Response(
            {"error": "Código incorrecto"},
            status=status.HTTP_400_BAD_REQUEST
        )

    usuario = User.objects.get(email=correo)
    usuario.set_password(nueva_contrasena)
    usuario.save()

    cache.delete(f"recuperacion_{correo}")

    return Response({"mensaje": "Contraseña actualizada correctamente"})

