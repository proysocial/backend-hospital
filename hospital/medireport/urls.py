from django.urls import path

# ── Auth & usuarios ──────────────────────────────────────────────
from medireport.views.login import login_por_correo
from medireport.views.registro import registrar_usuario
from medireport.views.recuperacion import (
    enviar_codigo_recuperacion,
    cambiar_contrasena,
)

# ── Perfil & contraseña directa ──────────────────────────────────
from medireport.views.perfil import EditarPerfilView, CambiarContrasenaDirectaView

# ── Dashboard & métricas ─────────────────────────────────────────
from medireport.views.report.metrics import MetricsDashboardView, AreasListView, AreaDetalleView
from medireport.views.report.txt_upload import UploadTXTView
from medireport.views.clear_registros import ClearRegistroTXT

# ── Reportes guardados ───────────────────────────────────────────
from medireport.views.report.reportes_guardados import (
    ReporteGuardadoListCreateView,
    ReporteGuardadoDetailView,
    MisReportesView,
    PublicarReporteView,
    ReportesPublicosView,
    ReportePublicoDetalleView,
)

# ── Docs ─────────────────────────────────────────────────────────
from medireport.views.docs import DocsView


urlpatterns = [
    # ── Documentación ──────────────────────────────────────────────
    path('docs/', DocsView.as_view(), name='api-docs'),

    # ── Auth & Registro ────────────────────────────────────────────
    path('registro/',                        registrar_usuario,            name='registro'),
    path('login/',                           login_por_correo,             name='login'),
    path('recuperar/enviar-codigo/',         enviar_codigo_recuperacion,   name='recuperar-enviar'),
    path('recuperar/cambiar-contrasena/',    cambiar_contrasena,           name='recuperar-cambiar'),

    # ── Perfil del usuario autenticado ─────────────────────────────
    path('perfil/',                          EditarPerfilView.as_view(),            name='perfil'),
    path('cambiar-contrasena/',              CambiarContrasenaDirectaView.as_view(), name='cambiar-contrasena'),

    # ── Dashboard & métricas ───────────────────────────────────────
    path('upload-txt/',                      UploadTXTView.as_view(),       name='upload-txt'),
    path('metrics-dashboard/',               MetricsDashboardView.as_view(), name='metrics-dashboard'),
    path('areas/',                           AreasListView.as_view(),       name='areas-list'),
    path('area-detalle/',                    AreaDetalleView.as_view(),     name='area-detalle'),

    # ── Administración ─────────────────────────────────────────────
    path('clear-registros/',                 ClearRegistroTXT.as_view(),    name='clear-registros'),

    # ── Reportes públicos (sin auth) ───────────────────────────────
    path('reportes/publicos/',               ReportesPublicosView.as_view(),        name='reportes-publicos'),
    path('reportes/publicos/<int:pk>/',      ReportePublicoDetalleView.as_view(),   name='reportes-publicos-detail'),

    # ── Mis reportes (solo del usuario autenticado) ────────────────
    path('reportes/mis-reportes/',           MisReportesView.as_view(),             name='mis-reportes'),

    # ── Publicar / despublicar un reporte ──────────────────────────
    path('reportes/<int:pk>/publicar/',      PublicarReporteView.as_view(),         name='reportes-publicar'),

    # ── CRUD general de reportes ───────────────────────────────────
    path('reportes/',                        ReporteGuardadoListCreateView.as_view(), name='reportes-list'),
    path('reportes/<int:pk>/',               ReporteGuardadoDetailView.as_view(),     name='reportes-detail'),
]
