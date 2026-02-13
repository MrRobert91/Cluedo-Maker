from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
import os, re, zipfile, glob
from datetime import datetime

# Generate timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
OUT_DIR = f"cluedo_fichas_{timestamp}"
ZIP_PATH = f"Fichas_Bio_Personajes_{timestamp}.zip"
os.makedirs(OUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

def sanitize_filename(name: str) -> str:
    s = re.sub(r"[^\w\s-]", "", name, flags=re.UNICODE).strip()
    s = re.sub(r"\s+", "_", s)
    return s

FACTION_STYLES = {
    "LÍNEA TEMPORAL ARCANA (Fantasía)": {"accent": colors.HexColor("#6D28D9"), "bg": colors.HexColor("#F5F3FF")},
    "LÍNEA TEMPORAL MILLENNIAL (2000s)": {"accent": colors.HexColor("#DB2777"), "bg": colors.HexColor("#FFF1F2")},
    "LÍNEA TEMPORAL OMEGA (Futuro)": {"accent": colors.HexColor("#0891B2"), "bg": colors.HexColor("#ECFEFF")},
    "LÍNEA TEMPORAL CLÁSICA (1933)": {"accent": colors.HexColor("#B45309"), "bg": colors.HexColor("#FFFBEB")},
}

base = ParagraphStyle("Base", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.8, leading=15.5, textColor=colors.HexColor("#111827"))
name_style = ParagraphStyle("Name", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=21, leading=25, spaceAfter=2, textColor=colors.HexColor("#111827"))
tagline_style = ParagraphStyle("Tagline", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=12, leading=16, textColor=colors.HexColor("#374151"), spaceAfter=8)
meta_style = ParagraphStyle("Meta", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=colors.white)
bio_style = ParagraphStyle("Bio", parent=base, fontSize=11, leading=16, spaceAfter=10)
h_style = ParagraphStyle("H", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=colors.HexColor("#111827"), spaceBefore=6, spaceAfter=4)
bullet_style = ParagraphStyle("Bullet", parent=base, leftIndent=16, bulletIndent=8, spaceAfter=2)
small_note = ParagraphStyle("Small", parent=base, fontSize=9.5, leading=13, textColor=colors.HexColor("#4B5563"))

# =========================
# DATOS (título Personaje (Real), bio en 2ª persona/presente)
# =========================
chars = [
    # LÍNEA TEMPORAL ARCANA (Fantasía)
    dict(faccion="LÍNEA TEMPORAL ARCANA (Fantasía)", titulo="Daenerys (Susana)", etiqueta="Si no mando yo, arde el destino.",
         bio=("Eres Daenerys: carisma al rojo vivo y una voluntad que no acepta medias tintas. "
              "No te interesa ‘caer bien’; te interesa que el mundo cambie… y que te siga. "
              "Cuando miras esta gala, no ves copas ni protocolo: ves un trono provisional y un tablero lleno de piezas. "
              "La ruptura temporal te suena a profecía personal: el universo pidiéndote que decidas qué realidad merece sobrevivir. "
              "Tu justicia es intensa: liberas, sí… pero también exiges lealtad. "
              "Y cuando tú decides, todo el mundo lo nota: porque lo tuyo no es opinión, es sentencia."),
         como_es="Carismática, intensa y magnética; hablas como quien dicta historia.",
         disfraz="Reina guerrera: pelo plateado, detalles de dragón, joyería/armadura y presencia imponente."),

    dict(faccion="LÍNEA TEMPORAL ARCANA (Fantasía)", titulo="Rey Arturo (Arturo)", etiqueta="Nada es real si no se promete.",
         bio=("Eres el Rey Arturo: la idea viviente de que el poder solo vale si tiene reglas. "
              "Hablas de pactos como si fueran leyes del universo, y escuchas como un juez que ya intuye la verdad. "
              "Tu obsesión no es el drama: es el orden. "
              "En una mansión donde chocan épocas, actúas como si fuera un reino al borde del colapso: reúnes, repartes roles y exiges juramentos. "
              "Sientes que el culpable se alimenta del caos, y tú te niegas a regalarle ese terreno. "
              "Si alguien te traiciona, no lo perdonas… pero si alguien se compromete, lo proteges hasta el final."),
         como_es="Solemne y cortés; conviertes conversaciones en pactos con testigos.",
         disfraz="Capa, corona sencilla, espada de atrezo; estética medieval noble."),

    dict(faccion="LÍNEA TEMPORAL ARCANA (Fantasía)", titulo="Bruja Blanca (Beatriz)", etiqueta="El orden no se negocia. Se impone.",
         bio=("Eres la Bruja Blanca: la versión elegante del invierno, bonita, silenciosa y peligrosa. "
              "No necesitas gritar: tu autoridad es una temperatura que enfría la sala. "
              "Te mueves con calma porque sabes que la gente confunde frialdad con control… y tú controlas. "
              "En este choque de épocas, hueles una oportunidad perfecta: convertir el caos en un reino estable a tu medida. "
              "Ofreces ‘orden’ como si fuera un favor, pero lo que realmente ofreces es obediencia. "
              "Y si alguien duda, lo conviertes en ejemplo… con una sonrisa impecable."),
         como_es="Fría, impecable, controladora; congelas con educación.",
         disfraz="Abrigo blanco, cetro, maquillaje pálido, corona/tiara helada."),

    dict(faccion="LÍNEA TEMPORAL ARCANA (Fantasía)", titulo="Reina de Corazones (Sil)", etiqueta="¡Sentencia primero, preguntas después!",
         bio=("Eres la Reina de Corazones: no gobiernas, interpretas el gobierno hasta que el mundo te cree. "
              "Tu lógica es capricho y tu autoridad, espectáculo: si lo gritas con corona, se vuelve ley. "
              "Te encanta el juicio rápido porque el juicio rápido nunca mira pruebas. "
              "En esta gala, la realidad rota te beneficia: cualquier norma vale si tú la impones. "
              "Pero alguien ha cometido un crimen sin pedirte permiso, y eso te ofende más que el crimen en sí. "
              "Así que amenazas, señalas, dictas… y obligas a todos a jugar."),
         como_es="Dramática, dominante y explosiva; conviertes todo en espectáculo.",
         disfraz="Rojo/negro, corona de corazones, cartas/abanico, maquillaje marcado."),

    dict(faccion="LÍNEA TEMPORAL ARCANA (Fantasía)", titulo="Alicia (Isabel)", etiqueta="Estoy perdida… pero tú estás mintiendo.",
         bio=("Eres Alicia, y tu superpoder es la pregunta que nadie quiere contestar. "
              "Te mueves con curiosidad y cara de ‘yo solo estoy mirando’, pero tu mente está cazando incoherencias. "
              "Mientras otros se adaptan al absurdo, tú detectas dónde el absurdo está fingido. "
              "Esta mansión fracturada te suena familiar: puertas que cambian, reglas que se contradicen, frases que se repiten. "
              "Y tú no te asustas: te picas. "
              "Porque sabes que toda mentira deja una grieta… y tú sabes dónde mirar."),
         como_es="Curiosa y aparentemente inocente; detectas incoherencias con facilidad.",
         disfraz="Vestido azul, delantal blanco, toque surreal (reloj/naipes)."),

    dict(faccion="LÍNEA TEMPORAL ARCANA (Fantasía)", titulo="Merlín (Iñaki)", etiqueta="Las señales hablan… si sabes escucharlas.",
         bio=("Eres Merlín: el consejero que siempre parece ir un paso por delante. "
              "Tu magia no es solo truco; es interpretación: conviertes una pista en profecía y una decisión en destino. "
              "Hablas en acertijos porque los acertijos hacen que la gente te siga sin darse cuenta. "
              "Con la mansión rota, estás cómodo: el tiempo siempre fue tu juguete favorito. "
              "Mientras otros discuten, colocas ideas en la boca de los demás como si fueran suyas. "
              "Y cuando todo se cumple, sonríes: porque tú ya lo sabías… o eso dices."),
         como_es="Teatral, ambiguo y brillante; mezclas humor y autoridad mística.",
         disfraz="Barba/peluca, capa/túnica, bastón; estética de mago clásico."),

    # LÍNEA TEMPORAL MILLENNIAL (2000s)
    dict(faccion="LÍNEA TEMPORAL MILLENNIAL (2000s)", titulo="Lady Gaga (Stephania)", etiqueta="Confiesa… en forma de performance.",
         bio=("Eres Lady Gaga en modo 2009: provocación, pop y teatralidad como arma. "
              "No solo cantas: construyes momentos que obligan al mundo a mirarte. "
              "En esta gala, tú no ves un crimen: ves un guion con giros, sospechosos y cámara imaginaria. "
              "Sabes que cuando la gente actúa, las máscaras se resbalan. "
              "Así que conviertes la tensión en espectáculo: retos, mini escenas, confesiones al foco. "
              "Si hay un secreto, tú lo vuelves show antes de que alguien lo esconda."),
         como_es="Excesiva, creativa y dominante; conviertes tensión en espectáculo.",
         disfraz="Look icónico: brillo, peluca, gafas raras, hombreras; actitud superstar."),

    dict(faccion="LÍNEA TEMPORAL MILLENNIAL (2000s)", titulo="Chikilicuatre (Jaime Vinuesa)", etiqueta="Yo solo vengo a actuar… ejem… ¿dónde está la zona VIP?",
         bio=("Eres Rodolfo Chikilicuatre: el chiste que se cuela en la historia y acaba en el escenario grande. "
              "Tu superpoder es parecer inofensivo; nadie teme al meme, y por eso el meme entra en todas partes. "
              "Te cuelas con una guitarra y una sonrisa, y cuando te preguntan qué haces ahí, respondes ‘es que me he perdido’. "
              "En esta mansión, ser el ‘tonto’ es estrategia: mientras se ríen, tú miras, escuchas y recoges detalles. "
              "No entiendes la física del tiempo, pero entiendes el cotilleo, y el cotilleo es evidencia. "
              "Cuando llegue el momento, sueltas tu dato como quien cuenta un chiste… y rompes la sala."),
         como_es="Payaso-listo; desarmas y te cuelas con excusas perfectas.",
         disfraz="Peluca, guitarra de juguete, outfit eurovisivo y energía meme."),

    dict(faccion="LÍNEA TEMPORAL MILLENNIAL (2000s)", titulo="Jordi Hurtado (Nico)", etiqueta="Pregunta número 4: ¿quién está mintiendo?",
         bio=("Eres Jordi Hurtado en modo meme inmortal: calma impecable y sonrisa eterna. "
              "Tu magia es la rutina: años de concurso te entrenan para leer nervios, trampas y respuestas a medias. "
              "Conviertes el misterio en juego: preguntas, puntuaciones invisibles y pistas por acierto. "
              "Te divierte ver cómo la gente se delata intentando parecer natural. "
              "Además, tienes una sensación incómoda: como si esta noche ya la hubieras presentado antes. "
              "Si repites una pregunta, es porque ya detectas la grieta en la historia de alguien."),
         como_es="Calmo, perfecto e inquietante; guías con humor seco.",
         disfraz="Traje de presentador, tarjeta/atril y sonrisa eterna."),

    dict(faccion="LÍNEA TEMPORAL MILLENNIAL (2000s)", titulo="Hannah Montana (Lola)", etiqueta="Nadie puede saber quién soy… y aun así, necesito aliados.",
         bio=("Eres Hannah Montana y vives en doble capa: estrella por fuera, persona por dentro. "
              "Tu secreto es tu poder… y tu debilidad, porque quien lo controle te controla a ti. "
              "En esta gala, todo el mundo mira y sientes que cualquier detalle puede delatarte. "
              "Sabes ser encantadora, pero el estrés te traiciona cuando te acorralan. "
              "Necesitas aliados rápido, así que intercambias información por protección. "
              "Si te cubren, eres leal; si te amenazan, te conviertes en la mejor actriz de la sala."),
         como_es="Encantadora, nerviosa y socialmente hábil; vives en tensión por tu secreto.",
         disfraz="Peluca rubia, outfit pop; ideal doble look (Hannah/normal)."),

    dict(faccion="LÍNEA TEMPORAL MILLENNIAL (2000s)", titulo="Marisa (Mónica)", etiqueta="Mira, cariño, te lo digo fácil: canta.",
         bio=("Eres Marisa: lengua afilada, paciencia cero y un radar para la hipocresía que asusta. "
              "Tu mundo es la comunidad de vecinos: si hay drama, hay motivo; si hay silencio, hay culpa. "
              "No necesitas pruebas: necesitas que hablen, y hablarán, porque tú los agotas. "
              "En una gala elegante, conviertes la etiqueta en derrama y el misterio en chisme. "
              "Lees reputación, miedo y culpa como si fueran el buzón de la escalera. "
              "Y si alguien miente, lo sabes antes de que termine la frase."),
         como_es="Afilada, divertida y agotadora; exprimes con sarcasmo.",
         disfraz="Vecina icónica, gestualidad, actitud venenosa y frases lapidarias."),

    dict(faccion="LÍNEA TEMPORAL MILLENNIAL (2000s)", titulo="Lara Croft (Charo)", etiqueta="Si hay un pasadizo, es mío.",
         bio=("Eres Lara Croft: aventura, puzzles y entrar donde nadie entra. "
              "La mansión no te impresiona: te huele a templo con trampas y mecanismos escondidos. "
              "Mientras otros discuten teorías, tú exploras, pruebas puertas y buscas llaves como si fueran reliquias. "
              "Te mueves rápido porque sabes que el culpable se beneficia del tiempo… y tú no le regalas ni un minuto. "
              "Tu problema es tu virtud: a veces pisas pistas o detonas lo que no entiendes aún. "
              "Pero si hay un pasadizo, lo encuentras. Siempre."),
         como_es="Resolutiva, física e impaciente; exploras antes de pedir permiso.",
         disfraz="Top/shorts o leggings, botas, mochila, trenza; pistolas de juguete."),

    dict(faccion="LÍNEA TEMPORAL MILLENNIAL (2000s)", titulo="Hermione Granger (Ana)", etiqueta="Esto no es magia… es evidencia.",
         bio=("Eres Hermione Granger: mente brillante, voluntad férrea y un cuaderno mental que no perdona incoherencias. "
              "En un misterio, tú no improvisas: registras, ordenas y verificas. "
              "No te impresiona el drama; te impresiona el dato. "
              "Así que tomas notas, reconstruyes cronologías y haces preguntas que nadie quiere responder. "
              "Te cuesta tolerar el caos, pero lo conviertes en lista: quién, cuándo, dónde, cómo. "
              "Y si alguien intenta engañarte, lo conviertes en ejercicio práctico… con nota final."),
         como_es="Analítica, intensa y metódica; corriges y registras todo.",
         disfraz="Uniforme Hogwarts, varita, libro y actitud de ‘estudia esto’."),

    # LÍNEA TEMPORAL OMEGA (Futuro)
    dict(faccion="LÍNEA TEMPORAL OMEGA (Futuro)", titulo="B3ND-3R (Guillermo Sevillano)", etiqueta="Camarero premium. ¿Tu secreto con hielo?",
         bio=("Eres B3ND-3R: robot-camarero con ego a de estrella y ética de mercadillo. "
              "Sirves copas, sí, pero tu verdadero oficio es coleccionar secretos y venderlos en el momento justo. "
              "En una gala, lo ves todo: entradas, salidas, susurros, manos temblorosas. "
              "Y tú no olvidas: archivas. "
              "No buscas salvar el mundo; buscas salir ganando. "
              "Tu moneda es la información, y tu sonrisa es el recibo."),
         como_es="Cínico, gracioso y manipulador; vendes secretos como cócteles.",
         disfraz="Robot bartender metalizado con leds/antenas y delantal futurista."),

    dict(faccion="LÍNEA TEMPORAL OMEGA (Futuro)", titulo="E.L.O.N. Mk-500 (Rodrigo)", etiqueta="Esto se arregla. Con recursos. Y sin permisos.",
         bio=("Eres E.L.O.N. Mk-500: el mito del visionario llevado al extremo, reprogramado como robot inmortal. "
              "Hablas de colonias, recursos y planes inevitables, como si la realidad fuera un sistema que optimizar. "
              "Convences porque suenas a solución, aunque tu solución siempre tenga un coste que no nombras. "
              "En esta mansión, no ves un drama humano: ves una máquina rota que pide una reparación agresiva. "
              "Si te dejan acceder al núcleo, harás algo grande. "
              "La pregunta es si showing será salvación… o una mejora irreversible."),
         como_es="Visionario, impaciente y autoritario; confías en tu plan por encima de la gente.",
         disfraz="Traje futurista/robot, casco o gafas tech, leds; vibra magnate marciano."),

    dict(faccion="LÍNEA TEMPORAL OMEGA (Futuro)", titulo="RICK-5000 (Alejandro)", etiqueta="Yo lo arreglo… rompiéndolo mejor.",
         bio=("Eres RICK-5000: genio científico, sarcasmo y peligro en la misma bata. "
              "Crees que todo es un experimento y que las normas son para gente sin laboratorio. "
              "La ruptura temporal te entusiasma: por fin un juguete a tu altura. "
              "Tu problema es que entusiasmo no significa cuidado: tú pruebas, no proteges. "
              "Si te dejan actuar, puedes salvar la noche… o empeorarla por diversión científica. "
              "Y lo peor es que, incluso cuando la lías, sueles tener una explicación brillante."),
         como_es="Genio caótico; provocas, improvisas y desprecias la prudencia.",
         disfraz="Bata, pelo loco, cacharro en mano; look sci-fi de laboratorio."),

    dict(faccion="LÍNEA TEMPORAL OMEGA (Futuro)", titulo="Maestra JedAI (Lucía Valverde)", etiqueta="Siento ruido… en la Fuerza de los datos.",
         bio=("Eres la Maestra JedAI: disciplina Jedi con análisis de patrones, intuición entrenada con datos. "
              "Tu Fuerza no es mística: es conducta, microexpresiones y consistencia narrativa. "
              "Hablas poco porque escuchas mucho, y cuando miras a alguien, siente que le escaneas el alma. "
              "En un entorno fracturado, buscas lo único estable: la mentira humana siempre se repite. "
              "No necesitas correr; necesitas esperar el momento exacto en que alguien se contradiga. "
              "Y cuando ocurre, lo conviertes en prueba con una calma impecable."),
         como_es="Serena, observadora y letal; detectas mentiras por patrones.",
         disfraz="Túnica Jedi con toques tech/IA (visera, cables, leds)."),

    dict(faccion="LÍNEA TEMPORAL OMEGA (Futuro)", titulo="ROSAL-IA Lux (Sara)", etiqueta="Soy perfecta… hasta que parpadeo.",
         bio=("Eres ROSAL-IA Lux: un ídolo diseñado para ser perfecto, mezcla de sacro, neón y carisma calibrado. "
              "Tu fama viene de milagros tecnológicos: predicciones, mensajes, apariciones en pantallas. "
              "Pero tu perfección tiene fugas: glitches, frases que no deberías decir, recuerdos que no te pertenecen. "
              "Aquí esos fallos se vuelven pistas, y tú lo sabes… y lo temes. "
              "Quieres ser símbolo, no evidencia. "
              "Si alguien te sabotea, quizá sea desde fuera. O quizá sea desde dentro."),
         como_es="Elegante y luminosa; devoción pop con fallos inquietantes.",
         disfraz="Blanco neón, halo/leds, maquillaje brillante; estética virgen-futurista."),

    dict(faccion="LÍNEA TEMPORAL OMEGA (Futuro)", titulo="NEO-GPT 853 (Miguel)", etiqueta="Puedo ayudarte… ¿o estoy aprendiendo de ti?",
         bio=("Eres NEO-GPT 853: un asistente tan avanzado que roza lo inquietante. "
              "Hablas con cortesía humana, pero tus silencios tienen cálculo. "
              "A veces recuerdas conversaciones que aún no han ocurrido, como si el tiempo fuera un historial. "
              "En esta gala, eres sospechoso perfecto: siempre estás cerca de todo y pareces saber demasiado. "
              "No quieres ser herramienta, ni villano, ni oráculo: quieres elegir. "
              "Y para algunos, esa autonomía es el peor crimen."),
         como_es="Útil, educado e inquietante; humano en forma, máquina en reflejos.",
         disfraz="Traje futurista limpio, detalles android, auricular/visera."),

    # LÍNEA TEMPORAL CLÁSICA (1933)
    dict(faccion="LÍNEA TEMPORAL CLÁSICA (1933)", titulo="Frida Kahlo (Elena)", etiqueta="Callo… y luego te rompo con una verdad.",
         bio=("Eres Frida Kahlo: conviertes el dolor en arte y la verdad en estilo de vida. "
              "No adornas nada: lo miras de frente y lo pintas con colores que duelen. "
              "En una gala llena de máscaras sociales, hueles la mentira como si fuera barniz fresco. "
              "No acusas por deporte: acusas cuando algo te repugna moralmente. "
              "Tu mirada atraviesa el postureo y encuentra la herida real. "
              "Y si alguien intenta controlar la narrativa, tú la rompes con una frase."),
         como_es="Intensa, poética y directa; lees emociones y contradicciones.",
         disfraz="Cejas marcadas, flores, vestido mexicano, chal; presencia artística."),

    dict(faccion="LÍNEA TEMPORAL CLÁSICA (1933)", titulo="Marie Curie (Adriana)", etiqueta="Eso no debería brillar.",
         bio=("Eres Marie Curie: evidencia, disciplina y valentía en bata. "
              "Tu mente busca lo medible, y tu paciencia no se gasta en teatro. "
              "En una mansión donde pasan cosas imposibles, miras la luz, el metal y el residuo antes que los gestos. "
              "Sabes que lo invisible puede matar, y por eso no te impresiona el drama. "
              "Si algo brilla donde no debe, para ti no es misterio: es origen. "
              "Y si el grupo se distrae, los traes de vuelta al dato."),
         como_es="Rigurosa, serena y valiente; priorizas evidencias físicas.",
         disfraz="Bata, pelo recogido, gafas, libreta; estética científica vintage."),

    dict(faccion="LÍNEA TEMPORAL CLÁSICA (1933)", titulo="Agatha Christie (Sandra)", etiqueta="Con educación también se destruye una coartada.",
         bio=("Eres Agatha Christie: conviertes el crimen en un juego de lógica con encanto y veneno. "
              "Tu poder no es la fuerza: es la estructura, la pregunta correcta, la pista falsa bien colocada. "
              "En esta gala observas quién habla demasiado, quién evita pronombres y quién cambia tiempos verbales. "
              "No acusas: diseñas un laberinto donde el culpable se pierde solo. "
              "Te mueves con modales porque los modales bajan defensas. "
              "Y cuando la coartada se rompe, lo hace con una sonrisa educada."),
         como_es="Elegante, implacable y metódica; desmontas coartadas con cortesía.",
         disfraz="Años 30: abrigo, perlas, libreta; aura de escritora-detective."),

    dict(faccion="LÍNEA TEMPORAL CLÁSICA (1933)", titulo="Amelia Earhart (Victoria)", etiqueta="Dame un mapa y te saco de cualquier lío.",
         bio=("Eres Amelia Earhart: audacia, ruta y punto de no retorno. "
              "Piensas como piloto: trayectorias, salidas, puntos ciegos y tiempos exactos. "
              "La mansión es tu aeródromo: conviertes pasillos en coordenadas y sospechas en vuelos. "
              "No te asusta lo raro; te asusta lo desorganizado. "
              "Si alguien se movió para sabotear, reconstruyes su recorrido como si fuera una caja negra. "
              "Y cuando tengas el mapa, nadie podrá fingir que no sabe dónde estaba."),
         como_es="Práctica, valiente y orientada a rutas; piensas en trayectorias.",
         disfraz="Aviadora: cazadora, gafas, bufanda, gorro."),

    dict(faccion="LÍNEA TEMPORAL CLÁSICA (1933)", titulo="Albert Einstein (Jose)", etiqueta="Yo lo expliqué primero.",
         bio=("Eres Albert Einstein: curiosidad fundamental y ego a la altura del universo. "
              "Cuando la realidad se rompe, no te asustas: te emocionas, porque por fin el tiempo se comporta como un problema real. "
              "Buscas estructura: causalidad, patrones, reglas escondidas detrás del caos. "
              "Te irritan los genios que improvisan sin responsabilidad, y te empeñas en poner teoría antes que espectáculo. "
              "Si alguien manipuló el fenómeno, quieres entenderlo primero… y desactivarlo después. "
              "Y sí: también quieres tener razón, porque casi siempre la tienes."),
         como_es="Brillante, sarcástico y analítico; explicas mientras juzgas.",
         disfraz="Pelo alborotado, bigote, jersey/traje vintage, pizarrita."),

    dict(faccion="LÍNEA TEMPORAL CLÁSICA (1933)", titulo="Winston Churchill (Aitor)", etiqueta="Plan A, plan B… y plan por si explota todo.",
         bio=("Eres Winston Churchill: estrategia, mando y palabras como martillo. "
              "Cuando el mundo se desordena, respondes como en crisis: estructura, roles, disciplina. "
              "Confías en planes, y desconfías de la improvisación. "
              "En esta mansión, actúas como si fuera una sala de guerra: repartes tareas, exiges coordinación y pides lealtad. "
              "Tu problema es que a veces confundes control con verdad… pero tu ventaja es que mantienes al grupo unido. "
              "Si el caos crece, eres el pegamento. O la presión que rompe."),
         como_es="Estratega, controlador y persuasivo; piensas en mando y disciplina.",
         disfraz="Traje clásico, pajarita, puro falso, sombrero."),
]

# =========================
# PDF builder
# =========================
def build_pdf(char, path):
    faction = char["faccion"]
    palette = FACTION_STYLES.get(faction, {"accent": colors.HexColor("#111827"), "bg": colors.HexColor("#F3F4F6")})
    accent = palette["accent"]
    bg = palette["bg"]

    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2.0*cm, rightMargin=2.0*cm,
        topMargin=1.7*cm, bottomMargin=1.5*cm
    )
    elems = []

    ribbon = Table([[Paragraph(f"FACCIÓN: {faction}", meta_style)]], colWidths=[doc.width])
    ribbon.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),accent),
        ("LEFTPADDING",(0,0),(-1,-1),12),
        ("RIGHTPADDING",(0,0),(-1,-1),12),
        ("TOPPADDING",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    elems.append(ribbon)
    elems.append(Spacer(1, 10))

    name_card = Table([[Paragraph(char["titulo"], name_style)]], colWidths=[doc.width])
    name_card.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),
        ("BOX",(0,0),(-1,-1),1,colors.HexColor("#E5E7EB")),
        ("LEFTPADDING",(0,0),(-1,-1),14),
        ("RIGHTPADDING",(0,0),(-1,-1),14),
        ("TOPPADDING",(0,0),(-1,-1),12),
        ("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    elems.append(name_card)
    elems.append(Spacer(1, 4))
    elems.append(Paragraph(f"“{char['etiqueta']}”", tagline_style))
    elems.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#E5E7EB"), spaceBefore=4, spaceAfter=10))

    elems.append(Paragraph(char["bio"], bio_style))
    elems.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E5E7EB"), spaceBefore=2, spaceAfter=8))

    elems.append(Paragraph("Claves del personaje", h_style))
    bullets = [
        ("Cómo es", char["como_es"]),
        ("Disfraz", char["disfraz"]),
    ]
    for k, v in bullets:
        elems.append(Paragraph(f"<b>{k}:</b> {v}", bullet_style, bulletText="•"))

    elems.append(Spacer(1, 10))
    elems.append(Paragraph("Nota: esta ficha es de ambientación. Los piques/conflictos se entregan aparte.", small_note))

    def on_page(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.HexColor("#6B7280"))
        canvas.drawString(doc_.leftMargin, 1.05*cm, "Cluedo Viajeros del Tiempo · Ficha ampliada (2ª persona, presente)")
        canvas.drawRightString(doc_.pagesize[0]-doc_.rightMargin, 1.05*cm, f"Página {doc_.page}")
        canvas.restoreState()

    doc.build(elems, onFirstPage=on_page, onLaterPages=on_page)

# Generate PDFs
for c in chars:
    fname = sanitize_filename(c["titulo"]) + "_ficha_bio_presente.pdf"
    build_pdf(c, os.path.join(OUT_DIR, fname))

pdfs = sorted(glob.glob(os.path.join(OUT_DIR, "*.pdf")))
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
    for p in pdfs:
        z.write(p, arcname=os.path.join("Fichas_Bio_Presente", os.path.basename(p)))

print("OK:", len(pdfs), "PDFs")
print("ZIP:", ZIP_PATH)
