import json
import os

def create_final_json():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "characters_data.json")
    output_path = os.path.join(base_dir, "characters_with_items_final.json")
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} no encontrado.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        factions_data = json.load(f)

    # Manual mapping of items
    final_items = {
        # ARCANA
        "Daenerys (Susana)": {
            "nombre": "Dracarys",
            "tipo": "poder",
            "descripcion": "No amenazas en público. No discutes. No debates. Ordenas.",
            "reglas": "En privado, te acercas a alguien, dices su nombre y pronuncias “Dracarys”. Desde ese momento esa persona queda obligada a intentar matar a quien tú señales. Si decide no hacerlo, no muere… pero pagará el precio: perderá su voto final. Tu poder es invisible hasta que deja de serlo. Y si alguien descubre que estás moviendo los hilos, no volverás a pasar desapercibida."
        },
        "Reina de Corazones (Sil)": {
            "nombre": "¡Que le corten la cabeza!",
            "tipo": "arma",
            "descripcion": "No insinúas. No propones. Ejecutas.",
            "reglas": "En cualquier momento puedes señalar a alguien y gritar: “¡Que le corten la cabeza!”. La persona muere en ese instante. Pero no hay anonimato. No hay sombra. Es una ejecución pública. Todos sabrán que fuiste tú. Y cuando eliges gobernar a base de miedo, el miedo también puede volverse contra ti."
        },
        "Bruja Blanca (Beatriz)": {
            "nombre": "Congelar",
            "tipo": "poder",
            "descripcion": "No matas. Paralizas.",
            "reglas": "Elige a alguien y decláralo congelado durante cinco minutos. Puede hablar. Puede moverse. Pero no puede usar habilidades ni realizar acciones relacionadas con sus objetivos, ni ayudar a otros a cumplir los suyos. No deja cicatrices visibles… pero sí resentimiento."
        },
        "Merlín (Iñaki)": {
            "nombre": "Transmutación",
            "tipo": "poder",
            "descripcion": "El equilibrio de las fuerzas puede alterarse.",
            "reglas": "Puedes cambiar a una persona de facción. No es una sugerencia. Es una transformación real. Mover a alguien de su bando puede cambiar el rumbo del juego… y también la percepción que tengan de ti."
        },
        "Alicia (Isabel)": {
            "nombre": "Espejo",
            "tipo": "poder",
            "descripcion": "Las reglas no son tan rígidas como parecen.",
            "reglas": "Una vez en la partida puedes cambiar de facción. Decidir quién eres y con quién estás. Pero recuerda: cambiar de lado tiene consecuencias. No todo el mundo confía en quien ya ha cruzado una vez el espejo."
        },
        "Rey Arturo (Arturo)": {
            "nombre": "Juramento Inquebrantable",
            "tipo": "poder",
            "descripcion": "La palabra tiene peso.",
            "reglas": "Puedes obligar a alguien a jurar que realizará una acción concreta. Una vez pronunciado el juramento, debe cumplirse. No puedes pedir lo imposible. Pero lo que se jura… se cumple. Si al final del juego esa persona no ha cumplido su juramento, perderá su derecho a voto final. Y si abusas del honor ajeno, tu nombre dejará de significar justicia."
        },
        
        # MILLENNIAL
        "Lady Gaga (Stephania)": {
            "nombre": "Furor Intertemporal",
            "tipo": "poder",
            "descripcion": "El caos puede convertirse en espectáculo.",
            "reglas": "Puedes activar un juego especial enfrentando a tu equipo contra otro. Para activarlo debes avisar a los Agentes Temporales. Si tu equipo gana, obtiene un token. No es solo entretenimiento. Es influencia disfrazada de show."
        },
        "Hannah Montana (Lola)": {
            "nombre": "Doble Popularidad",
            "tipo": "poder",
            "descripcion": "Tienes dos caras. Y dos públicos.",
            "reglas": "En una decisión intermedia puedes emitir dos votos en lugar de uno. No es magia. Es influencia. Y cuando hablas, hay más de una voz detrás de ti."
        },
        "Marisa (Mónica)": {
            "nombre": "Chisme",
            "tipo": "poder",
            "descripcion": "Sabes cómo sacar información.",
            "reglas": "Puedes hacer una pregunta directa. La persona debe responderte con la verdad. Tu arma es insistir hasta que la verdad sale sola. (Ejemplos de preguntas válidas: “¿Tienes un recurso ahora mismo?”, “¿Has usado ya tu habilidad?”, “¿Has robado un recurso hoy?”)"
        },
        "Lara Croft (Charo)": {
            "nombre": "Instinto de Supervivencia",
            "tipo": "defensa",
            "descripcion": "No te quedas mirando cuando todo se derrumba.",
            "reglas": "Si estás presente cuando alguien va a morir, puedes intervenir y evitar esa muerte. Además, una vez en la partida, cuando vaya a ocurrir una muerte en tu presencia, puedes decidir si usas tu intervención para salvar a la persona que iba a morir o para salvarte a ti misma si eras tú quien iba a morir. No es discurso. Es reflejo. Y asumir ese riesgo puede cambiar cómo te miran después."
        },
        "Hermione Granger (Ana)": {
            "nombre": "Retroceso Temporal",
            "tipo": "poder",
            "descripcion": "El tiempo no es tan fijo como parece.",
            "reglas": "En cualquier momento puedes deshacer una muerte. Sin condiciones. Sin límite. Pero alterar el curso de los acontecimientos no es algo que pase desapercibido. Cuando reescribes la historia, alguien siempre lo nota."
        },
        "Jordi Hurtado (Nico)": {
            "nombre": "Inyección Regeneradora",
            "tipo": "poder",
            "descripcion": "Durante años te han estudiado. No por fama: por biología.",
            "reglas": "Nadie entiende por qué no envejeces, por qué sigues igual mientras el resto cae. De ese misterio han sacado algo real: una inyección regeneradora creada a partir de tu sangre y del patrón que explica tu “no envejecimiento”. Puedes otorgar inmunidad a otra persona. La próxima vez que deba morir, no morirá. No puedes usarla sobre ti mismo."
        },
        "Chikilicuatre (Jaime Vinuesa)": {
            "nombre": "Colado Profesional",
            "tipo": "poder",
            "descripcion": "No eras el favorito. No eras el elegido.",
            "reglas": "Pero como en Eurovisión… te colaste en el escenario y actuaste igual. Puedes participar en una prueba que no corresponde a tu facción. Eliges dentro de qué equipo compites. Si ese equipo gana, la facción obtiene el punto o token… y tú también cuentas como ganador: tú también obtienes token."
        },
        
        # NEÓN (OMEGA)
        "B3ND-3R (Guillermo Sevillano)": {
            "nombre": "Robo Limpio",
            "tipo": "poder",
            "descripcion": "No haces discursos. Aprovechas oportunidades.",
            "reglas": "Puedes robar un recurso de forma secreta. Si nadie lo ve… no pasó."
        },
        "E.L.O.N. Mk-500 (Rodrigo)": {
            "nombre": "Ventaja de Recursos",
            "tipo": "poder",
            "descripcion": "No juegas desde cero: nunca lo has hecho.",
            "reglas": "Llegas con ventaja porque tu mundo funciona así: recursos primero, moral después. Empiezas la partida con dos recursos."
        },
        "RICK-5000 (Alejandro)": {
            "nombre": "Protocolo",
            "tipo": "poder",
            "descripcion": "El caos necesita reglas. Aunque sean temporales.",
            "reglas": "Puedes declarar una norma que se aplicará durante cinco minutos. Debe ser validada por los Agentes Temporales antes de activarse. (Ejemplos de reglas válidas: “Durante 5 minutos no se pueden intercambiar recursos.” / “Durante 5 minutos nadie puede usar habilidades.” / “Durante 5 minutos no puede convocarse ninguna votación.”)"
        },
        "Maestra JedAI (Lucía Valverde)": {
            "nombre": "Cambiar el Destino",
            "tipo": "poder",
            "descripcion": "El futuro es flexible para quien sabe verlo.",
            "reglas": "Puedes cambiar tu carta de recurso por otra. No controlas a los demás. Controlas tu camino."
        },
        "ROSAL-IA Lux (Sara)": {
            "nombre": "Influencia",
            "tipo": "poder",
            "descripcion": "En el futuro sigues siendo tan influyente como ahora… solo que amplificada.",
            "reglas": "Tu presencia inclina decisiones sin que tengas que levantar la voz. Puedes influir en una decisión intermedia. Debe validarse por los Agentes Temporales antes de aplicarse. (Ejemplos de usos: forzar que una persona cambie su voto / impedir que alguien se abstenga / obligar a alguien a posicionarse)."
        },
        "NEO-GPT 853 (Miguel)": {
            "nombre": "Predicción de Recursos",
            "tipo": "poder",
            "descripcion": "Observas. Analizas. Calculas.",
            "reglas": "Puedes elegir a dos personas y preguntar a los agentes temporales qué recurso tienen. La información no hace ruido… pero cambia decisiones."
        },
        
        # CRÓNICA (CLÁSICA)
        "Frida Kahlo (Elena)": {
            "nombre": "Juego del Dibujo",
            "tipo": "poder",
            "descripcion": "El arte también es combate.",
            "reglas": "Puedes activar un juego creativo. Para activarlo debes avisar a los Agentes Temporales. Si tu equipo gana, suma un punto. Si pierde no pasa nada. A veces la imaginación decide más que la fuerza."
        },
        "Marie Curie (Adriana)": {
            "nombre": "Hipótesis",
            "tipo": "poder",
            "descripcion": "Nada se afirma sin comprobarse.",
            "reglas": "Puedes formular una hipótesis concreta y recibir una respuesta de sí o no. (Ejemplos de hipótesis: “¿Hay un impostor en mi facción?” / “¿Se ha usado alguna habilidad?”)"
        },
        "Agatha Christie (Sandra)": {
            "nombre": "Doble Interrogatorio",
            "tipo": "poder",
            "descripcion": "Con educación también se destruye una coartada.",
            "reglas": "Puedes hacer dos preguntas en voz alta a un jugador. Ese jugador está obligado a responder a una con la verdad y a la otra con una mentira. Debes ser hábil al plantear las preguntas para deducir cuál es la información real."
        },
        "Amelia Earhart (Victoria)": {
            "nombre": "Intercepción",
            "tipo": "poder",
            "descripcion": "Ves el movimiento antes que los demás. Y reaccionas.",
            "reglas": "Siempre que veas un intercambio, un robo o una carta de recurso en la mano de alguien, puedes interceptarlo y quedártelo. No puedes acumular más de tres recursos a la vez."
        },
        "Albert Einstein (Jose)": {
            "nombre": "Método Científico",
            "tipo": "poder",
            "descripcion": "Si algo no encaja, no se acepta.",
            "reglas": "Una vez en la partida puedes invalidar una acción o consecuencia del juego. No puedes invalidar la votación final. (Ejemplos: un robo / una muerte / un punto conseguido / un cambio de facción / activación de habilidad)."
        },
        "Winston Churchill (Aitor)": {
            "nombre": "Juicio",
            "tipo": "poder",
            "descripcion": "A veces no decide una persona. Decide la mayoría.",
            "reglas": "Señalas a alguien. Todos votan si vive o muere. La responsabilidad es colectiva. Pero la iniciativa fue tuya."
        }
    }

    final_result = {}
    
    for faction, characters in factions_data.items():
        final_result[faction] = []
        for char in characters:
            title = char["titulo"]
            item = final_items.get(title, {
                "nombre": "Habilidad Especial",
                "tipo": "poder",
                "descripcion": "Pendiente de definir.",
                "reglas": "Pendiente de definir."
            })
            
            new_char = char.copy()
            new_char["objetos"] = [item]
            final_result[faction].append(new_char)
            
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=4)
        
    print(f"OK: characters_with_items_final.json generado con éxito.")

if __name__ == "__main__":
    create_final_json()
