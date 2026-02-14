import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_items(num_items=5):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "characters_data.json")
    output_path = os.path.join(base_dir, "characters_with_items.json")
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} no encontrado. Ejecuta extract_chars.py primero.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        factions_data = json.load(f)

    print(f"Generando {num_items} objeto(s) por personaje...")

    # System prompt for structured generation
    system_prompt = (
        "Eres un diseñador experto en juegos de rol y Cluedo en vivo. "
        f"Tu tarea es generar EXACTAMENTE {num_items} OBJETO(S) único(s) para cada personaje de un juego de Cluedo. "
        "El objeto debe ser coherente con la biografía, el disfraz y el tono del personaje. "
        "Existen tres tipos de objetos: 'arma', 'defensa' o 'poder' (ej: poder de la verdad)."
        f"\nDebes devolver un JSON con la misma estructura que recibes (organizado por facciones), "
        "pero añadiendo a cada personaje un campo 'objetos' que sea una LISTA de objetos con esta estructura:\n"
        "[\n"
        "  {\n"
        "    'nombre': 'Nombre del objeto',\n"
        "    'tipo': 'arma' | 'defensa' | 'poder',\n"
        "    'descripcion': 'Descripción breve y narrativa',\n"
        "    'reglas': 'Regla de juego (ej: Si usas esto, alguien debe decir la verdad)'\n"
        "  }\n"
        "]"
    )

    user_prompt = f"Aquí están los personajes agrupados por facciones:\n{json.dumps(factions_data, ensure_ascii=False)}"

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini-2025-08-07",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
        print(f"OK: {num_items} objeto(s) por personaje generados y guardados en {output_path}")
        
    except Exception as e:
        print(f"Error llamando a OpenAI: {e}")

if __name__ == "__main__":
    # Por defecto 1, pero puedes cambiarlo aquí a 2, 3, etc.
    generate_items(num_items=1)
