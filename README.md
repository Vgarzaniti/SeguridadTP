# SeguridadTP — OWASP Top 10:2025 Interactive Lab

Laboratorio y simulador interactivo para la visualización, explotación controlada y mitigación de las vulnerabilidades más críticas de **OWASP Top 10 (Edición 2025)**, desarrollado para el trabajo práctico de seguridad en aplicaciones web.

---

## 🎯 Propósito del Proyecto

Aprender ciberseguridad memorizando definiciones teóricas genera una falsa sensación de entendimiento. El objetivo de este laboratorio es aplicar el principio **Conceptos > Código**: comprender en tiempo real cómo viaja una petición HTTP maliciosa, cómo falla la arquitectura del backend vulnerable y cómo una defensa en profundidad neutraliza el vector de ataque.

El simulador analiza tres de las categorías más representativas extraídas del informe **OWASP Top 10:2025** (elaborado sobre datos de más de 2.8 millones de aplicaciones y 248 debilidades de software CWE).

---

## 🛡️ Vulnerabilidades Seleccionadas

### 1. A01: Broken Access Control (Control de Acceso Defectuoso — IDOR)
* **Posición en el Top**: **#1** (Presente en el 100% de las aplicaciones evaluadas en la edición 2025).
* **Causa Raíz**: Confianza ciega en parámetros manipulables por el cliente (`GET /api/resumen-cuenta?acct=102`) sin contrastar la identidad del token de sesión contra la propiedad del recurso en el backend.
* **En el Simulador**: 
  * Permite al usuario autenticado (ID: 101) cambiar el parámetro en la barra de URL para consultar registros ajenos (ID: 102 de María Gómez o ID: 103 de Cuenta VIP).
  * En **Modo Vulnerable**, el servidor retorna los datos confidenciales con código `HTTP 200 OK`.
  * En **Modo Seguro**, el middleware RBAC bloquea la petición y responde con `HTTP 403 Forbidden`.

### 2. A05: Injection (Inyección SQL)
* **Posición en el Top**: **#5** (Mayor volumen histórico de CVEs asociados, con más de 44.000 registros).
* **Causa Raíz**: Concatenación dinámica de entradas de usuario directamente dentro del motor de base de datos sin parametrización ni saneamiento.
* **En el Simulador**:
  * Demuestra el bypass de autenticación inyectando `' OR '1'='1` o comentando la sentencia con `admin' --`.
  * Desglosa el árbol sintáctico de la consulta evaluada en el motor y explica por qué la condición booleana devuelve acceso como Superadministrador sin validar contraseñas.
  * En **Modo Seguro**, muestra el uso de sentencias preparadas (*Prepared Statements*), donde la entrada del usuario es tratada como un literal aislado inofensivo.

### 3. A07: Authentication Failures (Fallas de Autenticación & Fuerza Bruta)
* **Posición en el Top**: **#7** (Riesgo permanente que agrupa 36 debilidades CWE).
* **Causa Raíz**: Falta de límites de tasa (*rate limiting*), ausencia de autenticación multifactor (MFA) y uso de contraseñas débiles o patrones predecibles tras filtraciones (ej. `Winter2025` evolucionando a `Winter2026!`).
* **En el Simulador**:
  * Ejecuta una simulación de ataque automatizado por diccionario contra la cuenta `admin@empresa.com`.
  * En **Modo Vulnerable**, el servidor responde ilimitadamente hasta que el bot adivina la clave y compromete la sesión.
  * En **Modo Seguro**, se activa la política alineada a **NIST 800-63b**: tras 3 intentos fallidos la IP se suspende temporalmente con código `HTTP 429 Too Many Requests` y se exige validación por segundo factor (MFA).

---

## 🚀 Características Técnicas

* **Pipeline de Red en Tiempo Real**: Visualizador animado que traza el paquete desde el navegador del cliente hasta el backend y la base de datos, con animaciones de rechazo ante bloqueos defensivos.
* **Métricas en Vivo**: Cálculo dinámico de latencia simulada (`⏱ ms`) y tamaño del payload HTTP de respuesta.
* **Comparador de Código Fuente**: Visualización lado a lado de la implementación vulnerable frente al código defensivo de producción.
* **Sintetizador de Audio Nativo**: Efectos sonoros generados dinámicamente con la Web Audio API (sin archivos de audio externos).
* **Cero Dependencias**: Construido puramente en Vanilla JavaScript (ES6+), CSS3 moderno y HTML5 semántico.

---

## 💻 Cómo Ejecutar Localmente

### Opción 1: Servidor Local con Python (Recomendado)
Desde la terminal en el directorio del proyecto:
```bash
python -m http.server 3000
```
Abrir en el navegador: [http://localhost:3000](http://localhost:3000)

### Opción 2: Servidor con Node.js
```bash
npx serve .
```

### Opción 3: Apertura Directa en el Navegador
En Windows (PowerShell):
```powershell
Start-Process index.html
```
O simplemente haciendo doble clic en el archivo `index.html`.

---

---

## 👥 Integrantes del Equipo

* **Valentín Garzaniti**
* **Romeo Monfroglio**
* **Valentino Laure**
* **Joaquín Caputto**
* **Mauro Lista**

---

## 📊 Presentación en Diapositivas (PPTX)

El repositorio incluye la presentación **`OWASP_Top_10_2025_Presentacion.pptx`** (formato 16:9 con diseño dark cybersecurity), estructurada en 13 diapositivas con diagramas, tablas comparativas y casos reales:

1. **Portada**: Título oficial, subtítulo y badges elegantes con los 5 integrantes del equipo.
2. **Metodología y Métricas Gigantes**: Indicadores numéricos destacados sobre 2.8M+ de apps analizadas, 248 CWEs evaluadas y 100% de prevalencia en puestos clave.
3. **Fundamentos Arquitectónicos**: Fórmula conceptual de cálculo de Riesgo vs. Vulnerabilidad y superficie de ataque web.
4. **Tabla Comparativa Completa**: Matriz estructurada de los 10 riesgos (2025 vs. 2021) con códigos de color para categorías nuevas y ascensos.
5. **A01 Broken Access Control**: Layout analítico 60/40 con desglose de la petición HTTP y anatomía de un ataque IDOR mitigado con RBAC.
6. **A02 Security Misconfiguration**: Falla estructural de la complejidad cloud, errores habituales y endurecimiento con guías NIST/CIS.
7. **A03 Software Supply Chain Failures**: Caso de estudio del ciberataque a SolarWinds y controles mediante SBOM y Dependency-Track.
8. **A04 Cryptographic Failures**: Comparativa directa entre prácticas criptográficas inseguras vs. estándares modernos (TLS 1.3, CSPRNG y Argon2).
9. **A05 Injection**: Estadísticas históricas (+44.000 CVEs) y bloque de código comparativo entre concatenación insegura y Prepared Statements.
10. **A06 Insecure Design**: Principio "Conceptos > Código", análisis de fallas en la lógica de negocio (caso reservas masivas) y Threat Modeling.
11. **A07 Autenticación & A08 Integridad**: Credential stuffing (patrón `Winter2025` ➔ `Winter2026`), NIST 800-63b, firmas digitales y deserialización insegura.
12. **A09 Registro y Alertas & A10 Condiciones Excepcionales**: Importancia de alertas activas (caso filtración oculta 7 años) y prevención de fallas abiertas sin rollback transaccional.
13. **Conclusiones y Demostración en Vivo**: Pilares de desarrollo seguro y pase al laboratorio interactivo del proyecto.

---

## 📁 Estructura del Repositorio

```text
SeguridadTP/
├── index.html                           # Estructura semántica, paneles del laboratorio y vistas
├── styles.css                           # Diseño visual oscuro estilo Dashboard de Ciberseguridad
├── app.js                               # Lógica interactiva, motor de simulación y audio synth
├── OWASP_Top_10_2025_Presentacion.pptx  # Presentación en diapositivas para 5 integrantes
├── build_presentation.py                # Script generador automatizado de la presentación
└── README.md                            # Documentación académica y técnica del proyecto
```
