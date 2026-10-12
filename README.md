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

## 📊 Presentación Grupal (PPTX para 5 Expositores)

El repositorio incluye el archivo listo para presentar **`OWASP_Top_10_2025_Presentacion.pptx`** (formato 16:9 con estética oscura de ciberseguridad), distribuido en 13 diapositivas equilibradas entre 5 oradores:

1. **Orador 1 — Introducción y Estado del Arte**:
   * Qué es OWASP, espacio del problema (APIs, Cloud y CI/CD) y diferencia entre Riesgo vs. Vulnerabilidad.
   * Metodología de la edición 2025 (2.8M de apps, 248 CWEs) y cambios respecto a 2021.
2. **Orador 2 — Puestos #1 y #2 (Control de Acceso y Configuración)**:
   * **A01: Broken Access Control**: 100% de prevalencia, IDOR y absorción de SSRF.
   * **A02: Security Misconfiguration**: El salto del puesto 5 al 2 debido a la complejidad de la nube.
3. **Orador 3 — Puestos #3 y #4 (Cadena de Suministro y Criptografía)**:
   * **A03: Software Supply Chain Failures**: Nueva categoría 2025, caso SolarWinds y SBOM.
   * **A04: Cryptographic Failures**: Algoritmos obsoletos, números pseudoaleatorios y TLS.
4. **Orador 4 — Puestos #5 y #6 (Inyección y Diseño)**:
   * **A05: Injection**: Récord histórico con +44.000 CVEs (SQLi y XSS) y Prepared Statements.
   * **A06: Insecure Design**: Separar diseño de implementación, fallas de negocio y Threat Modeling.
5. **Orador 5 — Puestos #7 al #10 y Cierre con Demo**:
   * **A07** (Autenticación y Fuerza Bruta) & **A08** (Integridad y Deserialización).
   * **A09** (Alertas sobre Monitoreo) & **A10** (Condiciones Excepcionales y Fallas Abiertas).
   * Conclusiones generales y pase a la **Demostración en Vivo del Simulador Web**.

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
