from django.http import HttpResponse
from django.views import View


DOCS_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MediReport API — Documentación de Endpoints</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
      --bg: #0d1117;
      --surface: #161b22;
      --surface2: #1c2128;
      --border: #30363d;
      --text: #e6edf3;
      --muted: #7d8590;
      --accent: #2f81f7;
      --green: #3fb950;
      --yellow: #d29922;
      --red: #f85149;
      --purple: #bc8cff;
      --orange: #ffa657;
      --cyan: #39c5cf;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: 'Inter', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
    }

    header {
      background: linear-gradient(135deg, #1a2332 0%, #0d1117 100%);
      border-bottom: 1px solid var(--border);
      padding: 2rem 3rem;
      position: sticky;
      top: 0;
      z-index: 10;
      backdrop-filter: blur(10px);
    }

    header h1 {
      font-size: 1.6rem;
      font-weight: 700;
      background: linear-gradient(90deg, #2f81f7, #39c5cf);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    header p {
      color: var(--muted);
      font-size: 0.9rem;
      margin-top: 0.3rem;
    }

    .base-url {
      display: inline-block;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.2rem 0.7rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: var(--cyan);
      margin-top: 0.5rem;
    }

    main {
      max-width: 1000px;
      margin: 0 auto;
      padding: 2rem 3rem 4rem;
    }

    .section {
      margin-bottom: 3rem;
    }

    .section-title {
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--accent);
      margin-bottom: 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .section-title .icon {
      font-size: 1.2rem;
    }

    .endpoint {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      margin-bottom: 0.8rem;
      overflow: hidden;
      transition: border-color 0.2s;
    }

    .endpoint:hover {
      border-color: var(--accent);
    }

    .endpoint-header {
      display: flex;
      align-items: flex-start;
      gap: 1rem;
      padding: 1rem 1.2rem;
      cursor: pointer;
    }

    .method {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.22rem 0.55rem;
      border-radius: 5px;
      min-width: 58px;
      text-align: center;
      flex-shrink: 0;
      margin-top: 0.05rem;
    }

    .GET    { background: #12261e; color: var(--green);  border: 1px solid #2ea043; }
    .POST   { background: #1f2937; color: var(--accent); border: 1px solid #2f81f7; }
    .PUT    { background: #241f0c; color: var(--yellow); border: 1px solid #d29922; }
    .PATCH  { background: #1e1428; color: var(--purple); border: 1px solid #8957e5; }
    .DELETE { background: #2a0f0d; color: var(--red);   border: 1px solid #f85149; }

    .endpoint-info { flex: 1; }

    .endpoint-url {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9rem;
      color: var(--text);
    }

    .endpoint-desc {
      color: var(--muted);
      font-size: 0.82rem;
      margin-top: 0.3rem;
      line-height: 1.4;
    }

    .auth-badge {
      font-size: 0.7rem;
      background: #1f2937;
      border: 1px solid var(--accent);
      color: var(--accent);
      padding: 0.15rem 0.5rem;
      border-radius: 20px;
      flex-shrink: 0;
    }

    .auth-badge.public {
      border-color: var(--green);
      color: var(--green);
      background: #12261e;
    }

    .body-info {
      background: var(--surface2);
      border-top: 1px solid var(--border);
      padding: 0.8rem 1.2rem;
      font-size: 0.82rem;
    }

    .body-info strong {
      color: var(--muted);
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .body-info pre {
      font-family: 'JetBrains Mono', monospace;
      color: var(--orange);
      margin-top: 0.4rem;
      font-size: 0.8rem;
      white-space: pre-wrap;
    }

    .toc {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.2rem 1.5rem;
      margin-bottom: 2.5rem;
    }

    .toc h3 {
      font-size: 0.85rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 0.8rem;
    }

    .toc ul { list-style: none; }

    .toc li {
      padding: 0.2rem 0;
    }

    .toc a {
      color: var(--accent);
      text-decoration: none;
      font-size: 0.88rem;
    }

    .toc a:hover { text-decoration: underline; }

    footer {
      text-align: center;
      padding: 1.5rem;
      color: var(--muted);
      font-size: 0.8rem;
      border-top: 1px solid var(--border);
    }
  </style>
</head>
<body>

<header>
  <h1>⚕️ MediReport API</h1>
  <p>Documentación de todos los endpoints disponibles — Sistema de Reportes Clínicos</p>
  <span class="base-url">Base URL: /api/v1/</span>
</header>

<main>

  <div class="toc">
    <h3>📋 Índice de secciones</h3>
    <ul>
      <li><a href="#auth">🔐 Autenticación &amp; Usuarios</a></li>
      <li><a href="#perfil">👤 Perfil &amp; Contraseña</a></li>
      <li><a href="#reportes">📄 Reportes Guardados</a></li>
      <li><a href="#publicos">🌐 Reportes Públicos</a></li>
      <li><a href="#datos">📊 Métricas &amp; Dashboard</a></li>
      <li><a href="#admin">🛠 Administración</a></li>
    </ul>
  </div>

  <!-- AUTENTICACIÓN -->
  <div class="section" id="auth">
    <div class="section-title"><span class="icon">🔐</span> Autenticación &amp; Usuarios</div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method POST">POST</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/registro/</div>
          <div class="endpoint-desc">Registra un nuevo usuario en el sistema.</div>
        </div>
        <span class="auth-badge public">Público</span>
      </div>
      <div class="body-info">
        <strong>Body JSON</strong>
        <pre>{ "correo": "...", "contrasena": "...", "nombre": "...", "apellido": "..." }</pre>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method POST">POST</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/login/</div>
          <div class="endpoint-desc">Inicia sesión. Devuelve tokens JWT (access + refresh).</div>
        </div>
        <span class="auth-badge public">Público</span>
      </div>
      <div class="body-info">
        <strong>Body JSON</strong>
        <pre>{ "correo": "...", "contrasena": "..." }</pre>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method POST">POST</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/token/refresh/</div>
          <div class="endpoint-desc">Renueva el access token usando el refresh token.</div>
        </div>
        <span class="auth-badge public">Público</span>
      </div>
      <div class="body-info">
        <strong>Body JSON</strong>
        <pre>{ "refresh": "&lt;refresh_token&gt;" }</pre>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method POST">POST</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/recuperar/enviar-codigo/</div>
          <div class="endpoint-desc">Envía un código de recuperación de contraseña al correo registrado.</div>
        </div>
        <span class="auth-badge public">Público</span>
      </div>
      <div class="body-info">
        <strong>Body JSON</strong>
        <pre>{ "correo": "..." }</pre>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method POST">POST</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/recuperar/cambiar-contrasena/</div>
          <div class="endpoint-desc">Cambia la contraseña usando el código recibido por correo.</div>
        </div>
        <span class="auth-badge public">Público</span>
      </div>
      <div class="body-info">
        <strong>Body JSON</strong>
        <pre>{ "correo": "...", "codigo": "123456", "nueva_contrasena": "..." }</pre>
      </div>
    </div>
  </div>

  <!-- PERFIL -->
  <div class="section" id="perfil">
    <div class="section-title"><span class="icon">👤</span> Perfil &amp; Contraseña</div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method GET">GET</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/perfil/</div>
          <div class="endpoint-desc">Devuelve los datos del usuario autenticado (nombre, apellido, correo).</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method PUT">PUT</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/perfil/</div>
          <div class="endpoint-desc">Edita el perfil del usuario autenticado (nombre, apellido o correo).</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
      <div class="body-info">
        <strong>Body JSON (todos opcionales)</strong>
        <pre>{ "nombre": "...", "apellido": "...", "correo": "..." }</pre>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method POST">POST</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/cambiar-contrasena/</div>
          <div class="endpoint-desc">Cambia la contraseña del usuario autenticado directamente (sin código de correo).</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
      <div class="body-info">
        <strong>Body JSON</strong>
        <pre>{ "nueva_contrasena": "..." }</pre>
      </div>
    </div>
  </div>

  <!-- REPORTES -->
  <div class="section" id="reportes">
    <div class="section-title"><span class="icon">📄</span> Reportes Guardados (propietario)</div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method GET">GET</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/reportes/</div>
          <div class="endpoint-desc">Lista todos los reportes del sistema (metadata, sin datos pesados).</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method POST">POST</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/reportes/</div>
          <div class="endpoint-desc">Crea un nuevo reporte. El autor se asigna automáticamente desde el token JWT.</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
      <div class="body-info">
        <strong>Body JSON</strong>
        <pre>{ "nombre": "...", "descripcion": "...", "datos": { ... } }</pre>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method GET">GET</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/reportes/mis-reportes/</div>
          <div class="endpoint-desc">Devuelve únicamente los reportes creados por el usuario autenticado (privados + públicos).</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method GET">GET</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/reportes/&lt;id&gt;/</div>
          <div class="endpoint-desc">Detalle completo del reporte (incluye datos). Solo el propietario o si está publicado.</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method PUT">PUT</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/reportes/&lt;id&gt;/</div>
          <div class="endpoint-desc">Edita el nombre, descripción o datos de un reporte. Solo el propietario puede editar.</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
      <div class="body-info">
        <strong>Body JSON (todos opcionales)</strong>
        <pre>{ "nombre": "...", "descripcion": "...", "datos": { ... } }</pre>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method DELETE">DELETE</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/reportes/&lt;id&gt;/</div>
          <div class="endpoint-desc">Elimina un reporte. Solo el propietario puede eliminarlo.</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method PATCH">PATCH</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/reportes/&lt;id&gt;/publicar/</div>
          <div class="endpoint-desc">Publica o despublica un reporte. Si no se envía body, hace toggle. Solo el propietario puede hacerlo.</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
      <div class="body-info">
        <strong>Body JSON (opcional)</strong>
        <pre>{ "publicado": true }   ← o false para despublicar</pre>
      </div>
    </div>
  </div>

  <!-- REPORTES PÚBLICOS -->
  <div class="section" id="publicos">
    <div class="section-title"><span class="icon">🌐</span> Reportes Públicos</div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method GET">GET</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/reportes/publicos/</div>
          <div class="endpoint-desc">Lista todos los reportes marcados como públicos. Cualquiera puede verlos sin autenticación.</div>
        </div>
        <span class="auth-badge public">Público</span>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method GET">GET</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/reportes/publicos/&lt;id&gt;/</div>
          <div class="endpoint-desc">Detalle completo de un reporte público (datos incluidos). Sin autenticación.</div>
        </div>
        <span class="auth-badge public">Público</span>
      </div>
    </div>
  </div>

  <!-- MÉTRICAS -->
  <div class="section" id="datos">
    <div class="section-title"><span class="icon">📊</span> Métricas &amp; Dashboard</div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method GET">GET</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/metrics-dashboard/</div>
          <div class="endpoint-desc">Dashboard principal de KPIs y métricas clínicas con filtros opcionales.</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
      <div class="body-info">
        <strong>Query Params (todos opcionales)</strong>
        <pre>?area=RADIOLOGIA&servicio=RX&fecha_inicio=2024-01-01&fecha_fin=2024-12-31</pre>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method GET">GET</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/areas/</div>
          <div class="endpoint-desc">Lista todas las áreas de laboratorio disponibles con su total de exámenes.</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method GET">GET</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/area-detalle/</div>
          <div class="endpoint-desc">Drill-down de métricas para un área específica, con filtros opcionales de servicio.</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
      <div class="body-info">
        <strong>Query Params</strong>
        <pre>?area=RADIOLOGIA DIAGNOSTICA&servicio=RX TORAX</pre>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method POST">POST</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/upload-txt/</div>
          <div class="endpoint-desc">Carga masiva de datos desde archivos TXT (.txt) con formato clínico estandarizado.</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
      <div class="body-info">
        <strong>Form Data</strong>
        <pre>file: &lt;archivo.txt&gt;</pre>
      </div>
    </div>
  </div>

  <!-- ADMIN -->
  <div class="section" id="admin">
    <div class="section-title"><span class="icon">🛠</span> Administración</div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method DELETE">DELETE</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/clear-registros/</div>
          <div class="endpoint-desc">Elimina todos los registros TXT del sistema. Usar con precaución.</div>
        </div>
        <span class="auth-badge">🔒 JWT</span>
      </div>
    </div>

    <div class="endpoint">
      <div class="endpoint-header">
        <span class="method GET">GET</span>
        <div class="endpoint-info">
          <div class="endpoint-url">/api/v1/docs/</div>
          <div class="endpoint-desc">Esta página. Documentación interactiva de todos los endpoints disponibles.</div>
        </div>
        <span class="auth-badge public">Público</span>
      </div>
    </div>
  </div>

</main>

<footer>
  MediReport API — Sistema de Reportes Clínicos &nbsp;·&nbsp;
  Autenticación via <strong>Bearer JWT</strong> en header <code>Authorization</code>
</footer>

</body>
</html>
"""


class DocsView(View):
    """
    GET /api/v1/docs/
    Página de documentación de todos los endpoints de la API.
    """
    def get(self, request):
        return HttpResponse(DOCS_HTML, content_type='text/html; charset=utf-8')
