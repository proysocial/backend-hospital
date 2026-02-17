from django.urls import path
from medireport.views.login import login_por_correo
from medireport.views.registro import registrar_usuario
from medireport.views.recuperacion import (
    enviar_codigo_recuperacion,
    cambiar_contrasena
)
from medireport.views.report.metrics import MetricsDashboardView
from medireport.views.report.txt_upload import UploadTXTView
from medireport.views.clear_registros import ClearRegistroTXT

urlpatterns = [
    path('registro/', registrar_usuario),
    path('login/', login_por_correo),
    path('recuperar/enviar-codigo/', enviar_codigo_recuperacion),
    path('recuperar/cambiar-contrasena/', cambiar_contrasena),
    path("upload-txt/", UploadTXTView.as_view()),
    path("metrics-dashboard/", MetricsDashboardView.as_view()),
    path('clear-registros/', ClearRegistroTXT.as_view(), name='clear-registros'),
]
