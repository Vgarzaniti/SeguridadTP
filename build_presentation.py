import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Palette
    C_BG = RGBColor(11, 17, 32)          # #0B1120 Fondo principal
    C_CARD = RGBColor(19, 29, 51)        # #131D33 Tarjeta
    C_CARD_ALT = RGBColor(24, 37, 65)    # #182541 Tarjeta secundaria
    C_BORDER = RGBColor(36, 50, 77)      # #24324D Borde
    C_CYAN = RGBColor(6, 182, 212)       # #06B6D4 Cian
    C_BLUE = RGBColor(59, 130, 246)      # #3B82F6 Azul
    C_EMERALD = RGBColor(16, 185, 129)   # #10B981 Esmeralda
    C_CRIMSON = RGBColor(239, 68, 68)    # #EF4444 Rojo
    C_AMBER = RGBColor(245, 158, 11)     # #F59E0B Ámbar
    C_PURPLE = RGBColor(139, 92, 246)    # #8B5CF6 Violeta
    C_WHITE = RGBColor(241, 245, 249)    # #F1F5F9 Título
    C_TEXT = RGBColor(203, 213, 225)     # #CBD5E1 Texto principal
    C_MUTED = RGBColor(148, 163, 184)    # #94A3B8 Texto secundario
    C_CODE_BG = RGBColor(8, 12, 20)      # Fondo consola

    def bg(slide):
        s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        s.fill.solid()
        s.fill.fore_color.rgb = C_BG
        s.line.fill.background()
        return s

    def slide_header(slide, title, category="OWASP TOP 10:2025", accent=C_CYAN):
        # Category pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), Inches(3.4), Inches(0.35))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_CARD
        pill.line.color.rgb = accent
        pill.line.width = Pt(1)
        tf_p = pill.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.text = category.upper()
        p_p.font.size = Pt(10)
        p_p.font.bold = True
        p_p.font.color.rgb = accent
        p_p.alignment = PP_ALIGN.CENTER

        # Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.82), Inches(11.7), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    # =========================================================================
    # SLIDE 1: PORTADA ELEGANTE CON INTEGRANTES
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg(s1)

    # Decorative banner line
    dec = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(0.12), Inches(4.8))
    dec.fill.solid()
    dec.fill.fore_color.rgb = C_CYAN
    dec.line.fill.background()

    # Title box
    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.2), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "OWASP Top 10:2025"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf.add_paragraph()
    p2.text = "Análisis Exhaustivo de Riesgos en Aplicaciones Web & Mitigación Práctica"
    p2.font.size = Pt(20)
    p2.font.color.rgb = C_CYAN
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "Monografía Técnica y Demostración Interactiva sobre 2.8 Millones de Aplicaciones"
    p3.font.size = Pt(13)
    p3.font.color.rgb = C_MUTED
    p3.space_before = Pt(6)

    # Integrantes Card
    t_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.8), Inches(11.2), Inches(2.3))
    t_box.fill.solid()
    t_box.fill.fore_color.rgb = C_CARD
    t_box.line.color.rgb = C_BORDER
    t_box.line.width = Pt(1)
    tf_t = t_box.text_frame
    tf_t.margin_left = Inches(0.35)
    tf_t.margin_top = Inches(0.25)

    p_lbl = tf_t.paragraphs[0]
    p_lbl.text = "INTEGRANTES DEL EQUIPO:"
    p_lbl.font.size = Pt(11)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = C_AMBER
    p_lbl.space_after = Pt(12)

    # Member badges as horizontal pill shapes
    integrantes = [
        "Valentín Garzaniti",
        "Romeo Monfroglio",
        "Valentino Laure",
        "Joaquín Caputto",
        "Mauro Lista"
    ]
    pill_w = 2.05
    start_x = 1.45
    for i, name in enumerate(integrantes):
        m_pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(start_x + (i * 2.15)), Inches(4.7), Inches(pill_w), Inches(0.8))
        m_pill.fill.solid()
        m_pill.fill.fore_color.rgb = C_CARD_ALT
        m_pill.line.color.rgb = C_CYAN
        m_pill.line.width = Pt(1)
        tf_m = m_pill.text_frame
        tf_m.word_wrap = True
        tf_m.margin_top = Inches(0.12)
        p_m = tf_m.paragraphs[0]
        p_m.text = name
        p_m.font.size = Pt(12)
        p_m.font.bold = True
        p_m.font.color.rgb = C_WHITE
        p_m.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: BIG STATS & METODOLOGÍA (LAYOUT DE NÚMEROS GIGANTES)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    bg(s2)
    slide_header(s2, "Metodología y Alcance: ¿Cómo se construyó la Edición 2025?", "Datos y Estadísticas Globales", C_BLUE)

    stats = [
        ("2.8M+", "Aplicaciones Analizadas", "Estudio masivo provisto por firmas líderes como Veracode, Sonar y Contrast Security.", C_CYAN),
        ("248", "Debilidades CWE Evaluadas", "Agrupadas a partir de 589 debilidades iniciales hacia 10 categorías finales de riesgo.", C_BLUE),
        ("2", "Nuevas Categorías en 2025", "Fallas en Cadena de Suministro (A03) y Mal Manejo de Excepciones (A10).", C_AMBER),
        ("100%", "Prevalencia en Puesto #1 y #2", "El total de aplicaciones probadas presentó fallas en control de acceso y configuración.", C_CRIMSON)
    ]

    for i, (num, label, desc, col) in enumerate(stats):
        bx = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + (i * 2.95)), Inches(1.8), Inches(2.8), Inches(4.9))
        bx.fill.solid()
        bx.fill.fore_color.rgb = C_CARD
        bx.line.color.rgb = C_BORDER
        bx.line.width = Pt(1)
        tf_b = bx.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = Inches(0.2)
        tf_b.margin_right = Inches(0.2)
        tf_b.margin_top = Inches(0.3)

        p_num = tf_b.paragraphs[0]
        p_num.text = num
        p_num.font.size = Pt(36)
        p_num.font.bold = True
        p_num.font.color.rgb = col
        p_num.space_after = Pt(8)

        p_lbl = tf_b.add_paragraph()
        p_lbl.text = label
        p_lbl.font.size = Pt(13)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = C_WHITE
        p_lbl.space_after = Pt(12)

        p_desc = tf_b.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = C_MUTED
        p_desc.line_spacing = 1.25

    # =========================================================================
    # SLIDE 3: CONCEPTUAL HERO: RIESGO VS VULNERABILIDAD & ESPACIO DEL PROBLEMA
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    bg(s3)
    slide_header(s3, "Fundamentos Arquitectónicos: Riesgo vs. Vulnerabilidad", "Conceptos Fundamentales", C_EMERALD)

    # Formula Box across the top
    f_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(11.7), Inches(1.4))
    f_box.fill.solid()
    f_box.fill.fore_color.rgb = C_CARD_ALT
    f_box.line.color.rgb = C_EMERALD
    f_box.line.width = Pt(1)
    tf_f = f_box.text_frame
    tf_f.margin_top = Inches(0.2)
    tf_f.margin_left = Inches(0.4)
    p_f1 = tf_f.paragraphs[0]
    p_f1.text = "FÓRMULA CONCEPTUAL DE EVALUACIÓN OWASP:"
    p_f1.font.size = Pt(11)
    p_f1.font.bold = True
    p_f1.font.color.rgb = C_EMERALD
    p_f2 = tf_f.add_paragraph()
    p_f2.text = "RIESGO = Agente Atacante + Vector de Entrada + Facilidad de Explotación + Daño al Negocio"
    p_f2.font.size = Pt(16)
    p_f2.font.bold = True
    p_f2.font.color.rgb = C_WHITE
    p_f2.space_before = Pt(4)

    # 2 Comparison Columns Below
    c1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), Inches(5.7), Inches(3.5))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_CARD
    c1.line.color.rgb = C_BORDER
    tf_c1 = c1.text_frame
    tf_c1.margin_left = Inches(0.3)
    tf_c1.margin_top = Inches(0.25)
    p_c1_t = tf_c1.paragraphs[0]
    p_c1_t.text = "VULNERABILIDAD (Falla Técnica)"
    p_c1_t.font.size = Pt(14)
    p_c1_t.font.bold = True
    p_c1_t.font.color.rgb = C_AMBER
    p_c1_t.space_after = Pt(8)
    bullets_v = [
        "Debilidad interna en el código fuente, configuración o diseño del sistema.",
        "Existe de forma pasiva aunque nadie la esté explotando en este momento.",
        "Ejemplo: Un puerto innecesario abierto en un contenedor o una variable sin sanear."
    ]
    for b in bullets_v:
        p = tf_c1.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT
        p.space_after = Pt(6)

    c2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.3), Inches(5.7), Inches(3.5))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_CARD
    c2.line.color.rgb = C_BORDER
    tf_c2 = c2.text_frame
    tf_c2.margin_left = Inches(0.3)
    tf_c2.margin_top = Inches(0.25)
    p_c2_t = tf_c2.paragraphs[0]
    p_c2_t.text = "RIESGO (Impacto Real)"
    p_c2_t.font.size = Pt(14)
    p_c2_t.font.bold = True
    p_c2_t.font.color.rgb = C_CRIMSON
    p_c2_t.space_after = Pt(8)
    bullets_r = [
        "Mide la probabilidad y severidad de que un atacante comprometa activos críticos.",
        "El Top 10:2025 prioriza causas raíz: atacar el problema de fondo, no solo el bug sintáctico.",
        "Las aplicaciones web modernas integran APIs, Cloud y pipelines CI/CD que maximizan el riesgo."
    ]
    for b in bullets_r:
        p = tf_c2.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 4: TABLA COMPARATIVA COMPLETA (2025 vs 2021)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    bg(s4)
    slide_header(s4, "El Mapa Completo: Tabla Comparativa OWASP Top 10 (2025 vs. 2021)", "Evolución y Cambios de Puesto", C_BLUE)

    table_shape = s4.shapes.add_table(11, 4, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(1.1)  # Código
    tbl.columns[1].width = Inches(4.5)  # Categoría 2025
    tbl.columns[2].width = Inches(3.2)  # Cambio frente a 2021
    tbl.columns[3].width = Inches(2.9)  # Estado / Tipo

    headers = ["#", "Categoría (Edición 2025)", "Cambio frente a 2021", "Naturaleza del Riesgo"]
    for col_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CARD_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_CYAN

    data = [
        ("A01", "Broken Access Control (Control de Acceso)", "Sigue #1, absorbe SSRF", "100% de apps afectadas", C_CRIMSON),
        ("A02", "Security Misconfiguration (Configuración)", "Subió del puesto 5 al 2", "Complejidad Cloud / Defaults", C_CRIMSON),
        ("A03", "Software Supply Chain Failures", "NUEVA en 2025 (Ex-Componentes)", "Compilación / CI/CD / SBOM", C_AMBER),
        ("A04", "Cryptographic Failures (Fallas Criptográficas)", "Bajó del puesto 2 al 4", "TLS / Claves / Random débil", C_BLUE),
        ("A05", "Injection (Inyección SQL, XSS, etc.)", "Bajó del puesto 3 al 5", "+44.000 CVEs históricos", C_PURPLE),
        ("A06", "Insecure Design (Diseño Inseguro)", "Bajó del puesto 4 al 6", "Lógica de negocio y modelos", C_BLUE),
        ("A07", "Authentication Failures (Autenticación)", "Mismo puesto (7), cambió nombre", "Credential Stuffing / MFA", C_AMBER),
        ("A08", "Software or Data Integrity Failures", "Mismo puesto (8), cambió nombre", "Firmas / Deserialización", C_BLUE),
        ("A09", "Security Logging and Alerting Failures", "Mismo puesto (9), foco en Alertas", "Detección temprana", C_BLUE),
        ("A10", "Mishandling of Exceptional Conditions", "NUEVA en 2025 (24 debilidades)", "Falla abierta / Rollback", C_AMBER)
    ]

    for row_idx, (code, cat, change, nature, tag_col) in enumerate(data, start=1):
        for col_idx, text in enumerate([code, cat, change, nature]):
            cell = tbl.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.font.color.rgb = tag_col if col_idx in [0, 3] else C_TEXT
            if col_idx == 0:
                p.font.bold = True

    # =========================================================================
    # SLIDE 5: A01 BROKEN ACCESS CONTROL (HERO SPLIT 60/40 CON EJEMPLO IDOR)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    bg(s5)
    slide_header(s5, "A01: Control de Acceso Defectuoso (Broken Access Control)", "Puesto #1 — Riesgo Máximo", C_CRIMSON)

    # Left: Explanation (60%)
    l_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.9))
    l_card.fill.solid()
    l_card.fill.fore_color.rgb = C_CARD
    l_card.line.color.rgb = C_BORDER
    tf_l = l_card.text_frame
    tf_l.margin_left = Inches(0.35)
    tf_l.margin_top = Inches(0.3)
    p_lt = tf_l.paragraphs[0]
    p_lt.text = "¿POR QUÉ SIGUE LIDERANDO EL TOP 10?"
    p_lt.font.size = Pt(13)
    p_lt.font.bold = True
    p_lt.font.color.rgb = C_CRIMSON
    p_lt.space_after = Pt(10)

    bullets_a01 = [
        "Prevalencia Absoluta: El 100% de las aplicaciones analizadas registró fallas en esta categoría.",
        "Absorción de SSRF: En 2025, Server-Side Request Forgery se integró como defecto de acceso.",
        "Causa Fundamental: Falta de validación en los verbos POST, PUT y DELETE en APIs REST.",
        "El Error Clave: Confiar ciegamente en comprobaciones hechas en el navegador o enviar identificadores directos.",
        "Principio de Menor Privilegio: Si no se deniega el acceso por defecto, la aplicación es vulnerable."
    ]
    for b in bullets_a01:
        p = tf_l.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT
        p.space_after = Pt(8)

    # Right: IDOR Code / Request breakdown (40%)
    r_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(1.8), Inches(4.6), Inches(4.9))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = C_CODE_BG
    r_card.line.color.rgb = C_CRIMSON
    r_card.line.width = Pt(1)
    tf_r = r_card.text_frame
    tf_r.margin_left = Inches(0.3)
    tf_r.margin_top = Inches(0.25)
    p_rt = tf_r.paragraphs[0]
    p_rt.text = "ANATOMÍA DE UN ATAQUE IDOR"
    p_rt.font.size = Pt(12)
    p_rt.font.bold = True
    p_rt.font.color.rgb = C_AMBER
    p_rt.space_after = Pt(8)

    code_text = (
        "// 1. Petición del Cliente Manipulada:\n"
        "GET /api/v1/cuenta?acct=102 HTTP/1.1\n"
        "Cookie: user_session_id=101 (Juan)\n\n"
        "// 2. Falla del Backend Vulnerable:\n"
        "const id = req.query.acct; // Lee 102 directo\n"
        "const data = db.find({ id }); // ¡Sin check!\n"
        "return res.json(data); // HTTP 200 (Fuga)\n\n"
        "// 3. Mitigación Obligatoria (RBAC):\n"
        "if (req.user.acctId !== requestedId) {\n"
        "  return res.status(403).json({\n"
        "    error: 'Acceso Denegado'\n"
        "  });\n"
        "}"
    )
    p_code = tf_r.add_paragraph()
    p_code.text = code_text
    p_code.font.size = Pt(10.5)
    p_code.font.color.rgb = C_CYAN

    # =========================================================================
    # SLIDE 6: A02 CONFIGURACIÓN INCORRECTA (CONTRASTE CONFIG VS CÓDIGO)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    bg(s6)
    slide_header(s6, "A02: Configuración de Seguridad Incorrecta", "Ascenso al Puesto #2 — Falla Estructural", C_CRIMSON)

    # 3 Cards: Por qué subió, Vectores, Solución Hardening
    c_a02_1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.9))
    c_a02_1.fill.solid()
    c_a02_1.fill.fore_color.rgb = C_CARD
    c_a02_1.line.color.rgb = C_BORDER
    tf = c_a02_1.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "EL SALTO DEL PUESTO 5 AL 2"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CRIMSON
    p.space_after = Pt(8)
    items1 = [
        "100% de prevalencia en los sistemas analizados.",
        "Cambio de paradigma: El comportamiento real depende más de la infraestructura y cloud que del código.",
        "La proliferación de servicios nube y microservicios multiplica los errores humanos en settings."
    ]
    for it in items1:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(6)

    c_a02_2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.9))
    c_a02_2.fill.solid()
    c_a02_2.fill.fore_color.rgb = C_CARD
    c_a02_2.line.color.rgb = C_BORDER
    tf = c_a02_2.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "ERRORES MÁS FRECUENTES"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.space_after = Pt(8)
    items2 = [
        "Cuentas y claves por defecto jamás modificadas.",
        "Consolas de administración o endpoints de prueba habilitados en producción.",
        "Ausencia de cabeceras HTTP de seguridad (CSP, HSTS, X-Content-Type).",
        "Stack traces y versiones de frameworks expuestas en mensajes de error públicos."
    ]
    for it in items2:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(6)

    c_a02_3 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.9))
    c_a02_3.fill.solid()
    c_a02_3.fill.fore_color.rgb = C_CARD
    c_a02_3.line.color.rgb = C_BORDER
    tf = c_a02_3.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "HARDENING Y MITIGACIÓN"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p.space_after = Pt(8)
    items3 = [
        "Adopción de guías de endurecimiento oficiales de NIST y CIS Benchmarks.",
        "Infraestructura como Código (IaC) inmutable y auditada antes del deploy.",
        "Deshabilitar funciones y módulos innecesarios en imágenes de contenedores.",
        "Auditoría continua automatizada comparando contra líneas base."
    ]
    for it in items3:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(6)

    # =========================================================================
    # SLIDE 7: A03 SUPPLY CHAIN FAILURES (CASE STUDY SOLARWINDS & SBOM)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    bg(s7)
    slide_header(s7, "A03: Fallas en la Cadena de Suministro de Software", "Nueva Categoría 2025 (#3)", C_AMBER)

    # Top Half: Case Study Banner
    top_c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.2))
    top_c.fill.solid()
    top_c.fill.fore_color.rgb = C_CARD_ALT
    top_c.line.color.rgb = C_AMBER
    top_c.line.width = Pt(1)
    tf_top = top_c.text_frame
    tf_top.margin_left = Inches(0.35)
    tf_top.margin_top = Inches(0.2)
    p_t = tf_top.paragraphs[0]
    p_t.text = "CASO EMBLEMÁTICO: ATAQUE A SOLARWINDS (2019 - 2020)"
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = C_AMBER
    p_t.space_after = Pt(6)

    p_sol = tf_top.add_paragraph()
    p_sol.text = "Los atacantes no vulneraron la aplicación final del cliente: comprometieron el pipeline de compilación (build system) del proveedor. El software malicioso fue firmado con certificados legítimos y distribuido como actualización oficial, infectando a más de 18.000 organizaciones (incluyendo ministerios de EEUU y gigantes tecnológicos)."
    p_sol.font.size = Pt(11.5)
    p_sol.font.color.rgb = C_WHITE
    p_sol.line_spacing = 1.25

    # Bottom Half: 2 Cards (Causas vs Soluciones SBOM)
    b1 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(5.7), Inches(2.5))
    b1.fill.solid()
    b1.fill.fore_color.rgb = C_CARD
    b1.line.color.rgb = C_BORDER
    tf = b1.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "Puntos Ciegos de la Cadena de Suministro"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CRIMSON
    for item in [
        "No escanear dependencias transitivas ('las dependencias de las dependencias').",
        "Pipelines de CI/CD con menos protección que los servidores de producción.",
        "Parches aplicados con meses de demora tras publicarse los CVEs."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {item}"
        pi.font.size = Pt(10.5)
        pi.font.color.rgb = C_TEXT

    b2 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.5))
    b2.fill.solid()
    b2.fill.fore_color.rgb = C_CARD
    b2.line.color.rgb = C_BORDER
    tf = b2.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "Controles Defensivos Requeridos"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    for item in [
        "SBOM (Software Bill of Materials) automatizado en cada release.",
        "OWASP Dependency-Track y Dependency-Check integrados en CI/CD.",
        "Monitoreo continuo contra bases públicas de vulnerabilidades (NVD y OSV)."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {item}"
        pi.font.size = Pt(10.5)
        pi.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 8: A04 FALLAS CRIPTOGRÁFICAS (CONTRASTE INSEGURO VS MODERNO)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    bg(s8)
    slide_header(s8, "A04: Fallas Criptográficas", "Puesto #4 — Protección de Datos Sensibles", C_BLUE)

    # 2 Comparison Columns
    col_bad = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9))
    col_bad.fill.solid()
    col_bad.fill.fore_color.rgb = C_CARD
    col_bad.line.color.rgb = C_CRIMSON
    col_bad.line.width = Pt(1)
    tf = col_bad.text_frame
    tf.margin_left = Inches(0.35)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "PRÁCTICAS INSEGURAS COMUNES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_CRIMSON
    p.space_after = Pt(10)

    for item in [
        "Uso de algoritmos obsoletos o quebrados (MD5, SHA1, DES).",
        "Generadores de números pseudoaleatorios inadecuados (predictibilidad en tokens de sesión o reset de contraseña).",
        "Tráfico sensible transmitido en HTTP texto plano sin forzar TLS.",
        "Contraseñas hasheadas sin salt o con algoritmos ultrarrápidos vulnerables a fuerza bruta GPU.",
        "Claves y secretos guardados en código fuente o repositorios de control de versiones."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {item}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(6)

    col_good = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9))
    col_good.fill.solid()
    col_good.fill.fore_color.rgb = C_CARD
    col_good.line.color.rgb = C_EMERALD
    col_good.line.width = Pt(1)
    tf = col_good.text_frame
    tf.margin_left = Inches(0.35)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "ESTÁNDAR CRIPTOGRÁFICO EXIGIDO"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p.space_after = Pt(10)

    for item in [
        "Forzar TLS 1.3 en el 100% de los endpoints con cabecera HSTS activa.",
        "Generadores de números pseudoaleatorios criptográficamente seguros (CSPRNG).",
        "Funciones de derivación de claves diseñadas para passwords: Argon2id, bcrypt o PBKDF2.",
        "Gestores de secretos dedicados (HashiCorp Vault, AWS KMS) con rotación automática.",
        "Clasificación formal de datos según su sensibilidad en tránsito y reposo."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {item}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(6)

    # =========================================================================
    # SLIDE 9: A05 INJECTION (HISTÓRICO DE CVES & PREPARED STATEMENTS)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    bg(s9)
    slide_header(s9, "A05: Inyección (SQLi, XSS y Comandos)", "Puesto #5 — Mayor Volumen de CVEs", C_PURPLE)

    # Left: +44k CVEs Stat Box + Explanation
    left_b = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.0), Inches(4.9))
    left_b.fill.solid()
    left_b.fill.fore_color.rgb = C_CARD
    left_b.line.color.rgb = C_BORDER
    tf = left_b.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.3)

    p_cve = tf.paragraphs[0]
    p_cve.text = "+44.000"
    p_cve.font.size = Pt(38)
    p_cve.font.bold = True
    p_cve.font.color.rgb = C_PURPLE

    p_sub = tf.add_paragraph()
    p_sub.text = "CVEs Registrados Históricamente"
    p_sub.font.size = Pt(12)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_WHITE
    p_sub.space_after = Pt(12)

    for it in [
        "XSS (Cross-Site Scripting): Alta frecuencia, baja barrera (+30.000 registros).",
        "SQL Injection: Menor frecuencia pero con impacto de compromiso total (+14.000 registros).",
        "Causa Raíz: Enviar datos no confiables directamente a un intérprete (SQL, shell, DOM) sin separar código de datos.",
        "Variantes: SQL, NoSQL, comandos OS, LDAP y lenguajes de expresión."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(10.8)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(6)

    # Right: Code Diff / Visual Breakdown
    right_b = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.1), Inches(1.8), Inches(6.4), Inches(4.9))
    right_b.fill.solid()
    right_b.fill.fore_color.rgb = C_CODE_BG
    right_b.line.color.rgb = C_BORDER
    tf = right_b.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    p.text = "CONCATENACIÓN INSEGURA vs PREPARED STATEMENTS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(10)

    sqli_code = (
        "// ❌ CÓDIGO VULNERABLE (Concatenación Dinámica):\n"
        "const query = 'SELECT * FROM users WHERE user = \\'' \n"
        "              + userInput + '\\' AND pass = \\'' + passInput + '\\'';\n\n"
        "// Si el atacante envía: ' OR '1'='1\n"
        "// La consulta se transforma en:\n"
        "// WHERE user = '' OR '1'='1' (¡Verdadero para todas las filas!)\n\n"
        "// --------------------------------------------------\n\n"
        "// ✅ CÓDIGO SEGURO (Sentencia Parametrizada):\n"
        "const sql = 'SELECT * FROM users WHERE user = ? AND pass = ?';\n"
        "const [rows] = await db.execute(sql, [userInput, passInput]);\n\n"
        "// El motor compila el árbol sintáctico ANTES de recibir los datos.\n"
        "// El payload es tratado como texto literal inofensivo."
    )
    p_c = tf.add_paragraph()
    p_c.text = sqli_code
    p_c.font.size = Pt(10)
    p_c.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 10: A06 INSECURE DESIGN (CASO CINE & THREAT MODELING)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    bg(s10)
    slide_header(s10, "A06: Diseño Inseguro (Insecure Design)", "Puesto #6 — Principio 'Conceptos > Código'", C_PURPLE)

    # Top Quote
    q_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.3))
    q_card.fill.solid()
    q_card.fill.fore_color.rgb = C_CARD_ALT
    q_card.line.color.rgb = C_PURPLE
    q_card.line.width = Pt(1)
    tf = q_card.text_frame
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "«Un diseño inseguro no se soluciona con una implementación perfecta de código.»"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p_sub = tf.add_paragraph()
    p_sub.text = "Si los controles de seguridad nunca fueron concebidos en la arquitectura, la ausencia de bugs no evitará el ataque."
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_CYAN
    p_sub.space_before = Pt(4)

    # 2 Bottom Cards: Ejemplo Cine vs Threat Modeling
    b_cine = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.4), Inches(5.7), Inches(3.3))
    b_cine.fill.solid()
    b_cine.fill.fore_color.rgb = C_CARD
    b_cine.line.color.rgb = C_BORDER
    tf = b_cine.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "Ejemplo Real: Lógica de Reserva en Cines"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.space_after = Pt(8)
    for it in [
        "Descuento grupal habilitado a partir de 15 personas.",
        "Un atacante reserva 600 asientos en todas las funciones con pocas peticiones legítimas.",
        "Provoca una pérdida millonaria al bloquear ventas genuinas.",
        "La implementación técnica no tenía ningún bug de código; la falla fue puramente de diseño del negocio."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT

    b_sol = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.4), Inches(5.7), Inches(3.3))
    b_sol.fill.solid()
    b_sol.fill.fore_color.rgb = C_CARD
    b_sol.line.color.rgb = C_BORDER
    tf = b_sol.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "Estrategias de Diseño Seguro"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p.space_after = Pt(8)
    for it in [
        "Modelado de Amenazas (Threat Modeling) previo al inicio de desarrollo.",
        "Definición explícita de Casos de Abuso (Abuse Cases) junto a las historias de usuario.",
        "Límites de tasa de negocio (Rate Limiting en reservas, no solo en endpoints).",
        "Adopción del modelo de madurez de software seguro OWASP SAMM."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 11: A07 AUTHENTICATION & A08 INTEGRITY (SPLIT ASIMÉTRICO)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    bg(s11)
    slide_header(s11, "A07: Autenticación & A08: Integridad de Software y Datos", "Puestos #7 y #8", C_EMERALD)

    c_a07 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9))
    c_a07.fill.solid()
    c_a07.fill.fore_color.rgb = C_CARD
    c_a07.line.color.rgb = C_BORDER
    tf = c_a07.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "A07: FALLAS DE AUTENTICACIÓN"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.space_after = Pt(10)

    for it in [
        "36 grupos de debilidades asociadas en el reporte 2025.",
        "Ataques de Fuerza Bruta y Credential Stuffing automatizados.",
        "Patrón de contraseñas predecibles: de 'Winter2025' a 'Winter2026!' tras filtraciones.",
        "Sin bloqueo progresivo, el servidor opera como un 'oráculo' que valida credenciales robadas.",
        "Mitigación: Pautas NIST 800-63b, retrasos exponenciales y MFA (Autenticación Multifactor) obligatorio."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(8)

    c_a08 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9))
    c_a08.fill.solid()
    c_a08.fill.fore_color.rgb = C_CARD
    c_a08.line.color.rgb = C_BORDER
    tf = c_a08.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "A08: INTEGRIDAD DE SOFTWARE O DATOS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(10)

    for it in [
        "Asumir que código o artefactos externos son seguros sin validación criptográfica.",
        "Plugins o módulos importados de CDN no confiables.",
        "Actualizaciones automáticas aplicadas sin verificar firmas digitales.",
        "Deserialización Insegura: Modificación de objetos serializados que permite ejecución de código remoto (RCE).",
        "Mitigación: Firmas digitales, verificación de hashes de integridad y escáneres estáticos de deserialización."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(8)

    # =========================================================================
    # SLIDE 12: A09 LOGGING & A10 CONDICIONES EXCEPCIONALES (NOVEDAD 2025)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    bg(s12)
    slide_header(s12, "A09: Fallas de Registro y Alertas & A10: Condiciones Excepcionales", "Puestos #9 y #10 (Nueva Categoría)", C_EMERALD)

    c_a09 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9))
    c_a09.fill.solid()
    c_a09.fill.fore_color.rgb = C_CARD
    c_a09.line.color.rgb = C_BORDER
    tf = c_a09.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "A09: DE 'MONITOREO' A 'ALERTAS'"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(10)

    for it in [
        "Un registro pasivo no detiene ataques: si no hay alertas en tiempo real, las intrusiones pasan inadvertidas.",
        "Caso Real: Aseguradora de salud infantil con filtración no detectada durante más de 7 años (3.5 millones de niños expuestos).",
        "Honeytokens: Trampas con cebos sintéticos que disparan alertas con tasa casi cero de falsos positivos.",
        "Herramientas: Pila ELK (Elasticsearch, Logstash, Kibana) y planes de respuesta a incidentes NIST 800-61."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(8)

    c_a10 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9))
    c_a10.fill.solid()
    c_a10.fill.fore_color.rgb = C_CARD
    c_a10.line.color.rgb = C_BORDER
    tf = c_a10.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "A10: MAL MANEJO DE CONDICIONES EXCEPCIONALES (NUEVA)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CRIMSON
    p.space_after = Pt(10)

    for it in [
        "Nueva categoría en 2025: 24 debilidades orientadas a fallas lógicas y errores no controlados.",
        "Falla Abierta: Cuando el sistema ante una excepción queda en un estado inesperado que otorga acceso.",
        "Caso Transaccional: Débito en origen, crédito en destino y log. Si se interrumpe a mitad de camino sin rollback, se vulnera la consistencia financiera.",
        "Mitigación: Manejadores globales centralizados de excepciones, transacciones atómicas y límites de tasa/cuotas."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(8)

    # =========================================================================
    # SLIDE 13: CONCLUSIÓN & DEMOSTRACIÓN DEL SIMULADOR WEB
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    bg(s13)
    slide_header(s13, "Conclusiones del Estudio & Demostración Práctica en Vivo", "Cierre del Trabajo Práctico", C_CYAN)

    c_fin = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9))
    c_fin.fill.solid()
    c_fin.fill.fore_color.rgb = C_CARD
    c_fin.line.color.rgb = C_BORDER
    tf = c_fin.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "CONCLUSIONES DE LA INVESTIGACIÓN"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(10)

    for it in [
        "1. La seguridad no es una etapa final: debe integrarse por diseño desde la concepción de la arquitectura.",
        "2. La automatización de los atacantes exige defensas automáticas (CI/CD con SAST/DAST, SBOM y alertas).",
        "3. El código limpio no basta: la configuración cloud y la cadena de suministro son los vectores predominantes.",
        "4. El Top 10:2025 demuestra que corregir la causa raíz es el único camino sostenible en la industria."
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_TEXT
        pi.space_after = Pt(8)

    c_demo = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9))
    c_demo.fill.solid()
    c_demo.fill.fore_color.rgb = C_CARD_ALT
    c_demo.line.color.rgb = C_EMERALD
    c_demo.line.width = Pt(1)
    tf = c_demo.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "DEMO EN VIVO: SIMULADOR WEB (SeguridadTP)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p.space_after = Pt(10)

    for it in [
        "Plataforma interactiva para visualizar los 3 vectores clave:",
        "• Demo 1: Manipulación de Objeto Directo (IDOR / A01) con switch Vulnerable vs. RBAC.",
        "• Demo 2: Inyección SQL (A05) con desglose en vivo del AST y Prepared Statements.",
        "• Demo 3: Fuerza Bruta / Credential Stuffing (A07) con bloqueo NIST y MFA.",
        "Pipeline animado en tiempo real con medición de latencia y Web Audio API.",
        "Repositorio público: github.com/Vgarzaniti/SeguridadTP"
    ]:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = C_WHITE if "•" in it else C_TEXT
        pi.space_after = Pt(6)

    output_path = "OWASP_Top_10_2025_Presentacion.pptx"
    prs.save(output_path)
    print(f"Presentation successfully updated: {output_path}")

if __name__ == "__main__":
    create_deck()
