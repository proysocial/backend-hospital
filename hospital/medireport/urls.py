from django.urls import path
from medireport.views.login import login_por_correo
from medireport.views.registro import registrar_usuario
from medireport.views.recuperacion import (
    enviar_codigo_recuperacion,
    cambiar_contrasena
)

urlpatterns = [
    path('registro/', registrar_usuario),
    path('login/', login_por_correo),
    path('recuperar/enviar-codigo/', enviar_codigo_recuperacion),
    path('recuperar/cambiar-contrasena/', cambiar_contrasena),
]
