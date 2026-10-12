/**
 * OWASP Top 10:2025 - Interactive Security Simulator
 * Dynamic Network & Execution Pipeline Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  initTabNavigation();
  initA01Simulator();
  initA05Simulator();
  initA07Simulator();
});

/* ===================================================================
   0. AUDIO FEEDBACK SYNTHESIZER (Web Audio API - Zero External Assets)
   =================================================================== */
const SoundFX = (() => {
  let ctx = null;

  function getContext() {
    if (!ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) ctx = new AudioCtx();
    }
    if (ctx && ctx.state === 'suspended') {
      ctx.resume();
    }
    return ctx;
  }

  function playTone(freq, type, duration, gainVal = 0.08) {
    try {
      const audio = getContext();
      if (!audio) return;
      const osc = audio.createOscillator();
      const gain = audio.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, audio.currentTime);
      gain.gain.setValueAtTime(gainVal, audio.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + duration);
      osc.connect(gain);
      gain.connect(audio.destination);
      osc.start();
      osc.stop(audio.currentTime + duration);
    } catch {
      // Audio not permitted or supported; silent fallback
    }
  }

  return {
    click: () => playTone(600, 'sine', 0.05, 0.04),
    packet: () => playTone(950, 'sine', 0.06, 0.03),
    success: () => {
      playTone(523.25, 'triangle', 0.1, 0.06);
      setTimeout(() => playTone(659.25, 'triangle', 0.15, 0.06), 80);
    },
    blocked: () => {
      playTone(220, 'sawtooth', 0.15, 0.07);
      setTimeout(() => playTone(180, 'sawtooth', 0.2, 0.08), 100);
    },
    breach: () => {
      playTone(880, 'square', 0.12, 0.05);
      setTimeout(() => playTone(440, 'square', 0.25, 0.08), 100);
    }
  };
})();

/* ===================================================================
   1. TAB NAVIGATION
   =================================================================== */
function initTabNavigation() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      SoundFX.click();
      const targetId = btn.getAttribute('data-tab');

      tabButtons.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      tabPanels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.classList.add('active');
      }
    });
  });
}

/* ===================================================================
   2. SIMULADOR A01: BROKEN ACCESS CONTROL (IDOR)
   =================================================================== */
function initA01Simulator() {
  const toggle = document.getElementById('a01-toggle-secure');
  const modeText = document.getElementById('a01-mode-text');
  const inputId = document.getElementById('a01-input-id');
  const btnSend = document.getElementById('a01-btn-send');
  const spinner = document.getElementById('a01-spinner');
  const serverLog = document.getElementById('a01-server-log');
  const responseView = document.getElementById('a01-response-view');
  const statusPill = document.getElementById('a01-status-pill');
  const latencyBadge = document.getElementById('a01-latency');
  const sizeBadge = document.getElementById('a01-response-size');
  const codePreview = document.getElementById('a01-code-preview');
  const codeBadge = document.getElementById('a01-code-badge');
  const pills = document.querySelectorAll('.pill-btn[data-target-id]');

  // Pipeline elements
  const nodeClient = document.getElementById('a01-node-client');
  const nodeAuth = document.getElementById('a01-node-auth');
  const nodeDb = document.getElementById('a01-node-db');
  const packet1 = document.getElementById('a01-packet-1');
  const packet2 = document.getElementById('a01-packet-2');

  const mockAccounts = {
    101: {
      id: 101,
      owner: "Juan Pérez (Tu Cuenta)",
      email: "juan.perez@empresa.com",
      balance: "$1,450.00 USD",
      card: "**** **** **** 1289",
      secretData: "Operaciones estándar",
      isOwner: true
    },
    102: {
      id: 102,
      owner: "María Gómez",
      email: "maria.g@corporativo.com",
      balance: "$84,920.00 USD",
      card: "**** **** **** 9912",
      secretData: "Transferencias corporativas pendientes",
      isOwner: false
    },
    103: {
      id: 103,
      owner: "Carlos Méndez (Cuenta VIP)",
      email: "carlos.m@directorio.com",
      balance: "$350,000.00 USD",
      card: "**** **** **** 7741",
      secretData: "Historial de crédito y datos confidenciales",
      isOwner: false
    }
  };

  const VULNERABLE_CODE = `// BACKEND VULNERABLE (Control de Acceso Inexistente)
app.get('/api/v1/resumen-cuenta', async (req, res) => {
  const acctId = req.query.acct; // ❌ Confianza ciega en el parámetro de la URL

  // No se verifica si req.session.userId coincide con acctId
  const cuenta = await db.query('SELECT * FROM accounts WHERE id = ?', [acctId]);
  
  return res.json(cuenta); // 🚨 Expone cualquier registro que el cliente solicite
});`;

  const SECURE_CODE = `// BACKEND SEGURO (Validación de Autorización RBAC)
app.get('/api/v1/resumen-cuenta', authMiddleware, async (req, res) => {
  const requestedAcct = parseInt(req.query.acct, 10);
  const sessionUser = req.user; // ✅ Obtenido de forma segura del JWT verificado

  // Verificación estricta de propiedad o privilegios de administrador
  if (sessionUser.accountId !== requestedAcct && !sessionUser.isAdmin) {
    logger.warn(\`Violación IDOR: Usuario \${sessionUser.id} intentó acceder a cuenta \${requestedAcct}\`);
    return res.status(403).json({
      error: "Acceso denegado: No posee privilegios sobre este recurso."
    });
  }

  const cuenta = await db.query('SELECT * FROM accounts WHERE id = ?', [requestedAcct]);
  return res.json(cuenta);
});`;

  function updateA01CodeView() {
    const isSecure = toggle.checked;
    if (isSecure) {
      modeText.textContent = "Modo: Seguro (RBAC / Auth)";
      modeText.classList.add('secure-active');
      codeBadge.textContent = "Validación de Sesión Activa";
      codeBadge.className = "diff-tag secure-tag";
      codePreview.textContent = SECURE_CODE;
    } else {
      modeText.textContent = "Modo: Vulnerable (IDOR)";
      modeText.classList.remove('secure-active');
      codeBadge.textContent = "Código Vulnerable Activo";
      codeBadge.className = "diff-tag";
      codePreview.textContent = VULNERABLE_CODE;
    }
  }

  function resetPipeline() {
    [nodeClient, nodeAuth, nodeDb].forEach(n => {
      n.className = n.className.replace(/node-active|node-blocked|node-success/g, '').trim();
    });
    packet1.className = 'packet-tracer';
    packet2.className = 'packet-tracer';
  }

  async function executeA01Request() {
    SoundFX.click();
    btnSend.disabled = true;
    spinner.style.display = 'inline-block';
    statusPill.textContent = "En tránsito...";
    statusPill.className = "status-indicator";
    latencyBadge.textContent = "⏱ ...";

    resetPipeline();
    nodeClient.classList.add('node-active');

    const isSecure = toggle.checked;
    const reqId = parseInt(inputId.value, 10);
    const account = mockAccounts[reqId];
    const startTime = performance.now();

    // Step 1: Client -> Auth Gateway
    packet1.classList.add('flow-forward');
    SoundFX.packet();
    await new Promise(r => setTimeout(r, 260));
    packet1.classList.remove('flow-forward');

    if (isSecure) {
      nodeAuth.classList.add('node-active');

      if (!account || !account.isOwner) {
        // BLOCKED by Auth
        await new Promise(r => setTimeout(r, 120));
        nodeAuth.classList.remove('node-active');
        nodeAuth.classList.add('node-blocked');
        packet1.classList.add('flow-backward-blocked');
        SoundFX.blocked();

        const latency = Math.round(performance.now() - startTime);
        latencyBadge.textContent = `⏱ ${latency} ms`;
        sizeBadge.textContent = "128 B";
        statusPill.textContent = "HTTP 403 FORBIDDEN";
        statusPill.className = "status-indicator forbidden";

        serverLog.textContent = `[HTTP REQUEST RECEIVED]\nGET /api/v1/resumen-cuenta?acct=${reqId}\nHeader: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...\n\n[AUTH ENGINE EVALUATION]\nSession Account ID: 101 (Juan Pérez)\nTarget Account ID:  ${reqId}\nCheck: session.accountId !== targetAcct -> TRUE (VIOLACIÓN DE ACCESO)\n\n[RESPONSE DISPATCHED]\nStatus: 403 Forbidden\nCausa: Middleware RBAC denegó acceso a recurso IDOR no autorizado.`;

        responseView.innerHTML = `
          <div class="error-banner">
            <h5>⛔ HTTP 403 - Acceso Denegado</h5>
            <p>El token de sesión no posee autorización para consultar la cuenta <strong>#${reqId}</strong>.</p>
            <p><small>La regla de Control de Acceso (RBAC) bloqueó con éxito el ataque IDOR en el servidor.</small></p>
          </div>
        `;

        spinner.style.display = 'none';
        btnSend.disabled = false;
        return;
      }
    } else {
      // In vulnerable mode, auth is bypassed or nonexistent
      nodeAuth.classList.add('node-active');
      await new Promise(r => setTimeout(r, 100));
    }

    // Step 2: Auth Gateway -> Database
    packet2.classList.add('flow-forward');
    SoundFX.packet();
    await new Promise(r => setTimeout(r, 260));
    packet2.classList.remove('flow-forward');
    nodeDb.classList.add('node-success');

    const latency = Math.round(performance.now() - startTime);
    latencyBadge.textContent = `⏱ ${latency} ms`;

    if (!account) {
      statusPill.textContent = "HTTP 404 NOT FOUND";
      statusPill.className = "status-indicator warn";
      sizeBadge.textContent = "45 B";
      serverLog.textContent = `[DATABASE QUERY]\nSELECT * FROM accounts WHERE id = ${reqId};\nResultado: 0 registros encontrados.`;
      responseView.innerHTML = `
        <div class="error-banner">
          <h5>Error 404</h5>
          <p>No se encontró ninguna cuenta con el identificador ${reqId}.</p>
        </div>
      `;
    } else if (!isSecure && !account.isOwner) {
      // Breached IDOR
      SoundFX.breach();
      statusPill.textContent = "HTTP 200 OK (LEAK)";
      statusPill.className = "status-indicator forbidden";
      sizeBadge.textContent = "486 B";

      serverLog.textContent = `[HTTP REQUEST RECEIVED]\nGET /api/v1/resumen-cuenta?acct=${reqId}\nHeader: Cookie: session_id=sess_juan_perez_101\n\n[VULNERABLE HANDLER EXECUTED]\nQuery directa: SELECT * FROM accounts WHERE id = ${reqId}\n⚠ ADVERTENCIA: No se validó la pertenencia del recurso contra la sesión.\n\n[RESPONSE DISPATCHED]\nStatus: 200 OK -> Entregando registro completo sin restricciones.`;

      responseView.innerHTML = `
        <div class="account-card-preview compromised">
          <div class="account-badge-header">
            <span class="danger-tag">🚨 DATOS DE TERCERO FILTRADOS (IDOR)</span>
            <span class="inline-code">CUENTA: #${account.id}</span>
          </div>
          <div class="field-line">Titular Expuesto: <strong>${account.owner}</strong></div>
          <div class="field-line">Email: <strong>${account.email}</strong></div>
          <div class="field-line">Saldo Revelado: <strong>${account.balance}</strong></div>
          <div class="field-line">Tarjeta: <strong>${account.card}</strong></div>
          <div class="field-line">Información Confidencial: <em>${account.secretData}</em></div>
        </div>
      `;
    } else {
      // Legitimate access
      SoundFX.success();
      statusPill.textContent = "HTTP 200 OK";
      statusPill.className = "status-indicator ok";
      sizeBadge.textContent = "380 B";

      serverLog.textContent = `[HTTP REQUEST RECEIVED]\nGET /api/v1/resumen-cuenta?acct=${reqId}\n\n[DATABASE QUERY]\nSELECT * FROM accounts WHERE id = ${reqId};\nValidación: Titular legítimo verificado con éxito.\n\n[RESPONSE DISPATCHED]\nStatus: 200 OK`;

      responseView.innerHTML = `
        <div class="account-card-preview valid">
          <div class="account-badge-header">
            <span>TITULAR: <strong>${account.owner}</strong></span>
            <span class="inline-code">TU CUENTA</span>
          </div>
          <div class="field-line">Email: <strong>${account.email}</strong></div>
          <div class="field-line">Saldo Disponible: <strong>${account.balance}</strong></div>
          <div class="field-line">Tarjeta: <strong>${account.card}</strong></div>
        </div>
      `;
    }

    spinner.style.display = 'none';
    btnSend.disabled = false;
  }

  // Event Listeners
  toggle.addEventListener('change', () => {
    SoundFX.click();
    updateA01CodeView();
    resetPipeline();
  });

  btnSend.addEventListener('click', executeA01Request);

  pills.forEach(p => {
    p.addEventListener('click', () => {
      SoundFX.click();
      inputId.value = p.getAttribute('data-target-id');
      executeA01Request();
    });
  });

  updateA01CodeView();
}

/* ===================================================================
   3. SIMULADOR A05: INJECTION (SQL INJECTION)
   =================================================================== */
function initA05Simulator() {
  const toggle = document.getElementById('a05-toggle-secure');
  const modeText = document.getElementById('a05-mode-text');
  const inputUser = document.getElementById('a05-input-user');
  const inputPass = document.getElementById('a05-input-pass');
  const btnExec = document.getElementById('a05-btn-exec');
  const spinner = document.getElementById('a05-spinner');
  const queryRender = document.getElementById('a05-query-render');
  const logicExpl = document.getElementById('a05-logic-expl');
  const terminalResult = document.getElementById('a05-terminal-result');
  const uiResult = document.getElementById('a05-ui-result');
  const statusPill = document.getElementById('a05-status-pill');
  const latencyBadge = document.getElementById('a05-latency');
  const codePreview = document.getElementById('a05-code-preview');
  const codeBadge = document.getElementById('a05-code-badge');
  const pills = document.querySelectorAll('.pill-btn[data-sqli-user]');

  // Pipeline elements
  const nodeClient = document.getElementById('a05-node-client');
  const nodeSanitizer = document.getElementById('a05-node-sanitizer');
  const nodeDb = document.getElementById('a05-node-db');
  const pipeStageLabel = document.getElementById('a05-pipe-stage');
  const packet1 = document.getElementById('a05-packet-1');
  const packet2 = document.getElementById('a05-packet-2');

  const VULNERABLE_CODE = `// CONSULTA INSEGURA (Concatenación Dinámica de Strings)
const username = req.body.username;
const password = req.body.password;

// ❌ Se concatenan directamente cadenas sin escapar ni parametrizar
const sql = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";

const [rows] = await db.query(sql); // El motor SQL ejecuta el payload como sintaxis`;

  const SECURE_CODE = `// CONSULTA SEGURA (Sentencia Parametrizada / Prepared Statement)
const username = req.body.username;
const password = req.body.password;

// ✅ Los placeholders (?) separan estrictamente el CÓDIGO de los DATOS
const sql = "SELECT id, username, role, password_hash FROM users WHERE username = ? LIMIT 1";

const [rows] = await db.execute(sql, [username]);
// La cadena inyectada se evalúa como texto literal inofensivo
const validPassword = await bcrypt.compare(password, rows[0]?.password_hash);`;

  function updateA05CodeView() {
    const isSecure = toggle.checked;
    if (isSecure) {
      modeText.textContent = "Modo: Seguro (Prepared Statement)";
      modeText.classList.add('secure-active');
      codeBadge.textContent = "Sentencia Parametrizada Activa";
      codeBadge.className = "diff-tag secure-tag";
      codePreview.textContent = SECURE_CODE;
      pipeStageLabel.textContent = "Prepared Statement";
    } else {
      modeText.textContent = "Modo: Vulnerable (Concatenación)";
      modeText.classList.remove('secure-active');
      codeBadge.textContent = "Concatenación Insegura";
      codeBadge.className = "diff-tag";
      codePreview.textContent = VULNERABLE_CODE;
      pipeStageLabel.textContent = "Parser SQL Directo";
    }
  }

  function resetPipeline() {
    [nodeClient, nodeSanitizer, nodeDb].forEach(n => {
      n.className = n.className.replace(/node-active|node-blocked|node-success/g, '').trim();
    });
    packet1.className = 'packet-tracer';
    packet2.className = 'packet-tracer';
  }

  async function executeA05Simulation() {
    SoundFX.click();
    btnExec.disabled = true;
    spinner.style.display = 'inline-block';
    statusPill.textContent = "Analizando AST...";
    statusPill.className = "status-indicator";
    latencyBadge.textContent = "⏱ ...";

    resetPipeline();
    nodeClient.classList.add('node-active');

    const isSecure = toggle.checked;
    const userVal = inputUser.value;
    const passVal = inputPass.value;
    const startTime = performance.now();

    const hasSqliPattern = userVal.includes("' OR '1'='1") ||
                           userVal.includes("' OR 1=1") ||
                           userVal.includes("' or '1'='1") ||
                           userVal.includes("' or 1=1") ||
                           userVal.includes("'--");

    // Step 1: Form -> SQL Engine
    packet1.classList.add('flow-forward');
    SoundFX.packet();
    await new Promise(r => setTimeout(r, 240));
    packet1.classList.remove('flow-forward');
    nodeSanitizer.classList.add('node-active');

    // Step 2: SQL Engine -> Database Execution
    packet2.classList.add('flow-forward');
    SoundFX.packet();
    await new Promise(r => setTimeout(r, 240));
    packet2.classList.remove('flow-forward');
    nodeDb.classList.add('node-active');

    const latency = Math.round(performance.now() - startTime);
    latencyBadge.textContent = `⏱ ${latency} ms`;

    if (!isSecure) {
      // VULNERABLE PATH
      queryRender.innerHTML = `
        <span class="sql-kw">SELECT</span> * <span class="sql-kw">FROM</span> users 
        <span class="sql-kw">WHERE</span> username = '<span class="sql-injected">${escapeHtml(userVal)}</span>' 
        <span class="sql-kw">AND</span> password = '<span class="sql-str">${escapeHtml(passVal)}</span>';
      `;

      if (hasSqliPattern) {
        SoundFX.breach();
        nodeSanitizer.classList.add('node-blocked');
        nodeDb.classList.add('node-blocked');
        statusPill.textContent = "SQLI BYPASS EXITOSO";
        statusPill.className = "status-indicator forbidden";

        logicExpl.innerHTML = `
          <strong>¿Por qué se rompe la lógica?</strong> Al inyectar comillas simples y <code class="inline-code">OR '1'='1'</code>, el predicado SQL evalúa <code class="inline-code">WHERE (falso) OR (VERDADERO)</code>. El motor ignora el password y devuelve todos los registros, concediendo acceso a la primera fila (superusuario).
        `;
        terminalResult.textContent = `[SQL PARSER WARNING]\nConsulta compilada con fragmentos de sintaxis inyectados por el usuario.\n\n[MOTOR DE CONSULTAS EJECUTADO]\nMatched Row 1: { id: 1, username: 'admin', role: 'SUPERADMIN', email: 'root@empresa.com' }\nTotal filas coincidentes: 1\n-> Sesión iniciada automáticamente como Administrador.`;

        uiResult.innerHTML = `
          <div class="account-card-preview compromised">
            <div class="account-badge-header">
              <span class="danger-tag">🔓 BYPASS TOTAL DE AUTENTICACIÓN</span>
              <span class="inline-code">ROL: SUPERADMIN</span>
            </div>
            <div class="field-line">Sesión forzada como: <strong>Administrador del Sistema</strong></div>
            <div class="field-line">Impacto: <strong>Control absoluto de la aplicación</strong></div>
          </div>
        `;
      } else if (userVal === "admin" && passVal === "clave123") {
        SoundFX.success();
        nodeDb.classList.add('node-success');
        statusPill.textContent = "LOGIN VÁLIDO";
        statusPill.className = "status-indicator ok";
        logicExpl.innerHTML = `Consulta normal con credenciales correctas.`;
        terminalResult.textContent = `[SQL EXECUTION OK]\n1 row matched: { id: 1, username: 'admin', role: 'ADMIN' }`;
        uiResult.innerHTML = `
          <div class="account-card-preview valid">
            <div class="account-badge-header">
              <span>INICIO DE SESIÓN CORRECTO</span>
            </div>
            <div class="field-line">Usuario: <strong>admin</strong></div>
          </div>
        `;
      } else {
        SoundFX.blocked();
        statusPill.textContent = "LOGIN FALLIDO";
        statusPill.className = "status-indicator warn";
        logicExpl.innerHTML = `Credenciales incorrectas sin inyección SQL válida.`;
        terminalResult.textContent = `[SQL EXECUTION]\n0 rows returned. (Credenciales no coinciden)`;
        uiResult.innerHTML = `
          <div class="error-banner">
            <h5>Credenciales Inválidas</h5>
            <p>Usuario o clave incorrectos.</p>
          </div>
        `;
      }
    } else {
      // SECURE PATH (Prepared Statements)
      queryRender.innerHTML = `
        <span class="sql-kw">PREPARE</span> stmt <span class="sql-kw">FROM</span> 
        'SELECT id, username, role FROM users WHERE username = <span class="sql-param">?</span> AND password = <span class="sql-param">?</span>';<br>
        <span class="sql-kw">EXECUTE</span> stmt <span class="sql-kw">USING</span> 
        '<span class="sql-str">${escapeHtml(userVal)}</span>', '<span class="sql-str">${escapeHtml(passVal)}</span>';
      `;

      logicExpl.innerHTML = `
        <strong>¿Por qué es seguro?</strong> El motor compila la sintaxis SQL <em>antes</em> de inyectar los datos. El texto del payload se trata como valor literal aislado, por lo que nunca altera la estructura de la consulta.
      `;

      if (userVal === "admin" && passVal === "clave123") {
        SoundFX.success();
        nodeSanitizer.classList.add('node-success');
        nodeDb.classList.add('node-success');
        statusPill.textContent = "LOGIN VÁLIDO";
        statusPill.className = "status-indicator ok";
        terminalResult.textContent = `[PREPARED STATEMENT EXECUTED]\nParam 1: 'admin'\nResultado: 1 usuario autenticado correctamente.`;
        uiResult.innerHTML = `
          <div class="account-card-preview valid">
            <div class="account-badge-header">
              <span>AUTENTICACIÓN SEGURA</span>
            </div>
            <div class="field-line">Usuario verificado: <strong>admin</strong></div>
          </div>
        `;
      } else {
        SoundFX.blocked();
        nodeSanitizer.classList.add('node-success');
        statusPill.textContent = "ATAQUE NEUTRALIZADO";
        statusPill.className = "status-indicator ok";
        terminalResult.textContent = `[PREPARED STATEMENT OK]\nBuscando usuario con literal: "${userVal}"\nResultado: 0 coincidencias. (El payload no fue interpretado como código)`;
        uiResult.innerHTML = `
          <div class="error-banner" style="border-color: #10b981; background: rgba(16, 185, 129, 0.1); color: #6ee7b7;">
            <h5 style="color: #a7f3d0;">🛡️ Ataque Bloqueado</h5>
            <p>El payload fue neutralizado al tratarse como una cadena de texto inerte.</p>
          </div>
        `;
      }
    }

    spinner.style.display = 'none';
    btnExec.disabled = false;
  }

  function escapeHtml(text) {
    return text.replace(/[&<>"']/g, m => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    })[m]);
  }

  toggle.addEventListener('change', () => {
    SoundFX.click();
    updateA05CodeView();
    resetPipeline();
  });

  btnExec.addEventListener('click', executeA05Simulation);

  pills.forEach(p => {
    p.addEventListener('click', () => {
      SoundFX.click();
      inputUser.value = p.getAttribute('data-sqli-user');
      inputPass.value = p.getAttribute('data-sqli-pass');
      executeA05Simulation();
    });
  });

  updateA05CodeView();
}

/* ===================================================================
   4. SIMULADOR A07: AUTHENTICATION FAILURES (BRUTE FORCE / CREDENTIAL STUFFING)
   =================================================================== */
function initA07Simulator() {
  const toggle = document.getElementById('a07-toggle-secure');
  const modeText = document.getElementById('a07-mode-text');
  const btnStart = document.getElementById('a07-btn-start-attack');
  const btnReset = document.getElementById('a07-btn-reset');
  const attemptCounter = document.getElementById('a07-attempt-counter');
  const ratelimitStatus = document.getElementById('a07-ratelimit-status');
  const mfaStatus = document.getElementById('a07-mfa-status');
  const accountStatus = document.getElementById('a07-account-status');
  const progressBar = document.getElementById('a07-progress-bar');
  const logBadge = document.getElementById('a07-log-badge');
  const logList = document.getElementById('a07-log-list');
  const codePreview = document.getElementById('a07-code-preview');
  const codeBadge = document.getElementById('a07-code-badge');

  const passwordDictionary = [
    { pass: "123456", label: "Diccionario común" },
    { pass: "admin2024", label: "Variante clásica" },
    { pass: "Winter2025", label: "Contraseña filtrada el año pasado (del informe)" },
    { pass: "Winter2025!", label: "Variante con símbolo" },
    { pass: "Winter2026", label: "Patrón de cambio de año" },
    { pass: "Winter2026!", label: "CONTRASEÑA REAL ACTUAL DE LA VÍCTIMA" }
  ];

  const VULNERABLE_CODE = `// BACKEND VULNERABLE (Sin Límite de Tasa ni MFA)
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  // ❌ No hay limitador de peticiones (Rate Limiter)
  // ❌ Funciona como un "oráculo" que responde infinitas veces
  const user = await findUserByEmail(email);
  if (!user || !bcrypt.compareSync(password, user.passwordHash)) {
    return res.status(401).json({ error: "Credenciales inválidas" });
  }

  // ❌ Sin MFA para cuentas corporativas
  const token = jwt.sign({ id: user.id }, SECRET);
  return res.json({ token });
});`;

  const SECURE_CODE = `// BACKEND SEGURO (NIST 800-63b + Rate Limit + MFA)
import rateLimit from 'express-rate-limit';

// ✅ Máximo 3 intentos por IP/cuenta antes de bloqueo temporal
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 3,
  message: { error: "Demasiados intentos fallidos. Cuenta bloqueada temporalmente." }
});

app.post('/api/auth/login', loginLimiter, async (req, res) => {
  const { email, password } = req.body;
  const user = await verifyCredentials(email, password);

  // ✅ Segundo Factor Obligatorio (MFA)
  if (user.requiresMfa) {
    return res.status(200).json({ step: "MFA_REQUIRED", sessionTemp: user.tempToken });
  }
});`;

  let isRunning = false;

  function updateA07CodeView() {
    const isSecure = toggle.checked;
    if (isSecure) {
      modeText.textContent = "Modo: Seguro (Rate Limit + MFA)";
      modeText.classList.add('secure-active');
      codeBadge.textContent = "Defensa Progresiva Activa";
      codeBadge.className = "diff-tag secure-tag";
      codePreview.textContent = SECURE_CODE;
      ratelimitStatus.textContent = "ACTIVO (3 INTENTOS MÁX)";
      ratelimitStatus.className = "def-val badge-on";
      mfaStatus.textContent = "OBLIGATORIO";
      mfaStatus.className = "def-val badge-on";
      progressBar.classList.add('secure-bar');
    } else {
      modeText.textContent = "Modo: Vulnerable (Sin Límites)";
      modeText.classList.remove('secure-active');
      codeBadge.textContent = "Sin Rate Limiting";
      codeBadge.className = "diff-tag";
      codePreview.textContent = VULNERABLE_CODE;
      ratelimitStatus.textContent = "DESACTIVADO";
      ratelimitStatus.className = "def-val badge-off";
      mfaStatus.textContent = "NO";
      mfaStatus.className = "def-val badge-off";
      progressBar.classList.remove('secure-bar');
    }
  }

  function resetState() {
    isRunning = false;
    btnStart.disabled = false;
    attemptCounter.textContent = `0 / ${passwordDictionary.length}`;
    accountStatus.textContent = "ABIERTA";
    accountStatus.className = "def-val badge-ok";
    progressBar.style.width = "0%";
    logBadge.textContent = "Listo para ejecutar";
    logList.innerHTML = `<div class="log-entry system-msg">[SISTEMA] Laboratorio reiniciado. Presione "Iniciar Ataque" para evaluar el comportamiento.</div>`;
    updateA07CodeView();
  }

  async function runAttackSimulation() {
    if (isRunning) return;
    SoundFX.click();
    isRunning = true;
    btnStart.disabled = true;

    const isSecure = toggle.checked;
    logList.innerHTML = "";
    logBadge.textContent = "Ataque en progreso...";

    const appendLog = (html, className = "") => {
      const entry = document.createElement('div');
      entry.className = `log-entry ${className}`;
      entry.innerHTML = html;
      logList.appendChild(entry);
      logList.scrollTop = logList.scrollHeight;
    };

    appendLog(`[BOTNET] Iniciando ataque de fuerza bruta contra <strong>admin@empresa.com</strong>...`, 'system-msg');

    for (let i = 0; i < passwordDictionary.length; i++) {
      await new Promise(r => setTimeout(r, 460));
      const attemptNum = i + 1;
      const item = passwordDictionary[i];
      const percent = (attemptNum / passwordDictionary.length) * 100;
      progressBar.style.width = `${percent}%`;
      attemptCounter.textContent = `${attemptNum} / ${passwordDictionary.length}`;

      if (!isSecure) {
        // VULNERABLE: Endless attempts allowed
        if (item.pass === "Winter2026!") {
          SoundFX.breach();
          appendLog(`[${attemptNum}] POST /login -> Password: <code>${item.pass}</code> -> <strong>HTTP 200 OK</strong>`, 'pwned');
          appendLog(`🚨 <strong>[PWNED]</strong> Token JWT obtenido. La cuenta fue vulnerada sin que ninguna alarma se disparara.`, 'pwned');
          accountStatus.textContent = "COMPROMETIDA";
          accountStatus.className = "def-val badge-locked";
          logBadge.textContent = "Cuenta Hackeada";
          break;
        } else {
          SoundFX.packet();
          appendLog(`[${attemptNum}] POST /login -> Password: <code>${item.pass}</code> -> HTTP 401 Unauthorized (Intento fallido)`, 'fail');
        }
      } else {
        // SECURE: Rate Limiter triggers on attempt 4
        if (attemptNum <= 3) {
          SoundFX.packet();
          appendLog(`[${attemptNum}] POST /login -> Password: <code>${item.pass}</code> -> HTTP 401 (Intento ${attemptNum}/3)`, 'fail');
        } else {
          SoundFX.blocked();
          appendLog(`[${attemptNum}] POST /login -> Password: <code>${item.pass}</code> -> <strong>HTTP 429 TOO MANY REQUESTS</strong>`, 'blocked');
          appendLog(`🛡️ <strong>[BLOQUEO ACTIVO]</strong> IP atacante suspendida por 15 minutos según política NIST 800-63b.`, 'blocked');
          accountStatus.textContent = "PROTEGIDA / BLOQUEO ACTIVO";
          accountStatus.className = "def-val badge-locked";
          logBadge.textContent = "Ataque Mitigado";

          await new Promise(r => setTimeout(r, 500));
          appendLog(`[DEFENSA EN PROFUNDIDAD] Aún si el atacante obtuviera la contraseña real, se exige Código OTP Multifactor (MFA).`, 'mfa-prompt');
          break;
        }
      }
    }

    isRunning = false;
    btnStart.disabled = false;
  }

  toggle.addEventListener('change', () => {
    SoundFX.click();
    resetState();
  });

  btnStart.addEventListener('click', runAttackSimulation);
  btnReset.addEventListener('click', () => {
    SoundFX.click();
    resetState();
  });

  updateA07CodeView();
}
