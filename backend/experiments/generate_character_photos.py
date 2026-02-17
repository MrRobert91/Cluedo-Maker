"""
Script para generar fotos de personajes usando las fotos reales de los participantes.
Utiliza GPT Image 1.5 de OpenAI para transformar las fotos reales en los personajes asignados.
"""

import os
import json
import base64
import sys
from pathlib import Path
from openai import OpenAI
import re
import unicodedata
from datetime import datetime

# Configuración
SCRIPT_DIR = Path(__file__).parent
FOTOS_DIR = SCRIPT_DIR / "fotos"
OUTPUT_DIR = SCRIPT_DIR / "fotos" / "imagenes_generadas"
CHARACTERS_JSON = SCRIPT_DIR / "characters_with_objectives.json"
CHARACTERS_BIO_JSON = SCRIPT_DIR / "characters_with_items_final.json"

# Cargar API Key desde el archivo .env si existe
def load_api_key():
    """Carga la API key desde .env o variable de entorno."""
    # Primero intentar desde variable de entorno
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "tu-api-key-aqui":
        # Intentar cargar desde archivo .env en backend/
        env_file = SCRIPT_DIR.parent / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENAI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"')
                        break
    
    if not api_key or api_key == "tu-api-key-aqui":
        raise ValueError(
            "No se encontró la API key de OpenAI.\n"
            "Por favor configura OPENAI_API_KEY en el archivo backend/.env\n"
            "o como variable de entorno."
        )
    
    return api_key

OPENAI_API_KEY = load_api_key()
client = OpenAI(api_key=OPENAI_API_KEY)


def normalize_text(text):
    """Normaliza texto para comparaciones robustas (sin tildes, minúsculas, alfanumérico)."""
    text = unicodedata.normalize("NFD", str(text))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text).strip()
    return text


def extract_person_name(titulo):
    """Extrae el nombre de la persona entre paréntesis."""
    match = re.search(r'\(([^)]+)\)', titulo)
    return match.group(1) if match else None


def extract_character_name(titulo):
    """Extrae el nombre del personaje (sin paréntesis)."""
    return re.sub(r'\s*\([^)]+\)', '', titulo).strip()


def load_characters():
    """Carga los personajes desde el JSON."""
    # Cargar bios maestras desde characters_with_items_final.json
    bios_by_person = {}
    bios_by_character = {}
    if CHARACTERS_BIO_JSON.exists():
        with open(CHARACTERS_BIO_JSON, 'r', encoding='utf-8') as f_bio:
            bio_data = json.load(f_bio)

        for _timeline, _chars in bio_data.items():
            for _char in _chars:
                titulo_bio = _char.get('titulo', '')
                bio_text = _char.get('bio', '')
                person_bio = extract_person_name(titulo_bio)
                character_bio = extract_character_name(titulo_bio)

                if person_bio and bio_text:
                    bios_by_person[normalize_text(person_bio)] = bio_text
                if character_bio and bio_text:
                    bios_by_character[normalize_text(character_bio)] = bio_text

    with open(CHARACTERS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    characters = {}
    for timeline, chars in data.items():
        for char in chars:
            person_name = extract_person_name(char['titulo'])
            character_name = extract_character_name(char['titulo'])
            if person_name:
                # Prioridad: bio del archivo final de bios -> bio del JSON actual
                bio_from_final = bios_by_person.get(normalize_text(person_name)) or bios_by_character.get(normalize_text(character_name))
                final_bio = bio_from_final or char.get('bio', '')

                characters[person_name.lower()] = {
                    'character_name': character_name,
                    'person_name': person_name,
                    'disfraz': char['disfraz'],
                    'bio': final_bio,
                    'como_es': char['como_es'],
                    'etiqueta': char['etiqueta']
                }
    
    return characters


def find_matching_photo(person_name, fotos_dir):
    """Encuentra la foto correspondiente a una persona."""
    person_norm = normalize_text(person_name)
    person_tokens = person_norm.split()
    
    # Extensiones de imagen comunes
    extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    
    # Primera pasada: coincidencia fuerte por nombre completo normalizado
    for file in os.listdir(fotos_dir):
        file_path = fotos_dir / file
        if file_path.suffix.lower() not in [ext.lower() for ext in extensions]:
            continue

        file_name = os.path.splitext(file)[0]
        file_norm = normalize_text(file_name)
        file_norm = re.sub(r"\bfoto\b", "", file_norm).strip()

        if person_norm == file_norm or person_norm in file_norm or file_norm in person_norm:
            return file_path

    # Segunda pasada: coincidencia por primer nombre exacto (para casos tipo "jaime_foto")
    if person_tokens:
        first_name = person_tokens[0]
        for file in os.listdir(fotos_dir):
            file_path = fotos_dir / file
            if file_path.suffix.lower() not in [ext.lower() for ext in extensions]:
                continue

            file_name = os.path.splitext(file)[0]
            file_norm = normalize_text(file_name)
            file_tokens = [t for t in file_norm.split() if t != "foto"]

            if first_name in file_tokens:
                return file_path
    
    return None


def generate_character_prompt_dalle(character_data):
    """Genera el prompt para DALL-E 3 (generación sin foto base)."""
    prompt = f"""Professional photorealistic portrait of a person as {character_data['character_name']}.

Character costume and styling: {character_data['disfraz']}

Character personality and demeanor: {character_data['como_es']}

Comedic direction: push visual absurdity and humor with a ridiculous, expressive pose and a rich, over-the-top background full of funny details related to the character.
Goal: the image should provoke laughter at first glance while staying coherent with the character fantasy.

Photography style: Professional portrait, dramatic cinematic lighting, high quality photorealistic render, themed background appropriate to the character concept."""
    
    return prompt


def generate_character_prompt_gpt_image(character_data):
    """Genera el prompt para GPT Image 1.5 (edición de foto base)."""
    prompt = f"""Transform this person into {character_data['character_name']} while preserving their facial features and likeness.

CRITICAL: Keep the person's face, facial structure, eyes, nose, mouth, and overall facial characteristics completely intact. Only modify:
- Costume and clothing: {character_data['disfraz']}
- Styling and accessories as described in the costume
- Add a fun, playful background clearly related to the character theme and their backstory
- Lighting and atmosphere to match the character's personality

Framing and composition requirements (mandatory):
- Full-body shot: the person must be visible from head to toe.
- Face fully visible and never cropped.
- Leave clear headroom above the head (empty space on top of frame).
- Keep the head centered and comfortably inside the frame.
- Do not crop forehead, chin, hair, sides of the face, hands, or feet.

Character personality for reference (affects styling and mood, NOT facial features): {character_data['como_es']}

Character backstory and narrative context (use this to define scene mood, symbolism, and atmosphere, NOT to alter facial identity): {character_data['bio']}

Creative direction:
- VERY IMPORTANT: use a clearly funny, absurd, and intentionally ridiculous pose, while still coherent with the character.
- The character must be actively doing something (dynamic action, not static pose).
- Show the character doing an iconic or typical action for that role in an exaggerated comedic way.
- The character must be holding or using at least one representative but absurd prop/object linked to the character.
- Include absurd, harmless, laugh-out-loud background elements strongly tied to the character and bio context.
- Build a rich background with multiple humorous visual details (props, signs, objects, mini gags) that reward looking closely.
- Primary objective: make people burst out laughing when they see the image.
- Keep the scene readable, visually clear, and photorealistic.

Safety and style constraints: fully clothed, non-sexual, non-explicit, PG-13 tone.

The final image must be a photorealistic portrait where the original person is clearly recognizable, just dressed and styled as the character. High quality, professional photography, dramatic cinematic lighting."""
    
    return prompt


def generate_character_image_dalle3(photo_path, character_data):
    """Genera la imagen del personaje usando DALL-E 3 (sin usar la foto base)."""
    
    # Generar el prompt
    prompt = generate_character_prompt_dalle(character_data)
    
    print(f"Generando imagen para {character_data['person_name']} como {character_data['character_name']}...")
    print("Prompt completo:")
    print(prompt)
    
    try:
        # Usar la API de generación de imágenes con DALL-E 3
        print("Generando imagen con DALL-E 3...")
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="auto",
            n=1,
            quality="standard"
        )
        
        # Obtener la URL de la imagen generada
        image_url = response.data[0].url
        
        # Descargar la imagen desde la URL
        import requests
        image_response = requests.get(image_url)
        image_bytes = image_response.content
        
        # Convertir a base64 para mantener compatibilidad con el resto del código
        import base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        return image_base64
        
    except Exception as e:
        print(f"Error al generar imagen: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_character_image_gpt_image_15(photo_path, character_data):
    """Genera la imagen del personaje usando gpt-image-1.5 (editando la foto base)."""
    
    # Generar el prompt
    prompt = generate_character_prompt_gpt_image(character_data)
    
    print(f"Generando imagen para {character_data['person_name']} como {character_data['character_name']}...")
    print("Prompt completo:")
    print(prompt)

    def call_edit_api(edit_prompt):
        with open(photo_path, "rb") as image_file:
            return client.images.edit(
                model="gpt-image-1.5",
                image=[image_file],
                prompt=edit_prompt,
                size="1536x1024",
                quality="low"
                
            )
    
    try:
        print("Editando imagen con gpt-image-1.5...")

        response = call_edit_api(prompt)

        if hasattr(response.data[0], 'b64_json') and response.data[0].b64_json:
            image_base64 = response.data[0].b64_json
        else:
            raise ValueError("La respuesta de la API no contiene b64_json")
        
        return image_base64
        
    except Exception as e:
        error_text = str(e).lower()

        # Reintento automático con prompt más seguro si bloquea moderación
        if "moderation_blocked" in error_text or "safety" in error_text:
            try:
                print("[ADVERTENCIA] Bloqueo de seguridad detectado. Reintentando con prompt seguro...")
                safe_prompt = f"""Edit this portrait into the character {character_data['character_name']}.
Keep facial identity unchanged.
Use modest, fully clothed wardrobe inspired by: {character_data['disfraz']}.
Use a clean, playful, non-sexual, PG-13 cinematic style.
Avoid any suggestive or explicit elements.
"""

                response = call_edit_api(safe_prompt)
                if hasattr(response.data[0], 'b64_json') and response.data[0].b64_json:
                    return response.data[0].b64_json
            except Exception as retry_error:
                print(f"Error en reintento seguro: {retry_error}")

        print(f"Error al generar imagen: {e}")
        import traceback
        traceback.print_exc()
        return None


def save_base64_image(base64_data, output_path):
    """Guarda una imagen desde datos base64."""
    try:
        image_bytes = base64.b64decode(base64_data)
        with open(output_path, 'wb') as f:
            f.write(image_bytes)
        return True
    except Exception as e:
        print(f"Error guardando imagen: {e}")
        return False


def create_run_output_dir(base_output_dir):
    """Crea una carpeta de ejecución con formato generation-{n}_{fecha}."""
    base_output_dir.mkdir(exist_ok=True)

    run_numbers = []
    pattern = re.compile(r"^generation-(\d+)_")
    for item in base_output_dir.iterdir():
        if item.is_dir():
            match = pattern.match(item.name)
            if match:
                run_numbers.append(int(match.group(1)))

    next_run_number = (max(run_numbers) + 1) if run_numbers else 1
    run_timestamp = datetime.now().strftime("%d-%m-%Y--%H-%M")
    run_folder_name = f"generation-{next_run_number}_{run_timestamp}"

    run_output_dir = base_output_dir / run_folder_name
    run_output_dir.mkdir(exist_ok=False)

    return run_output_dir


class TeeStream:
    """Duplica la salida a consola y fichero."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def setup_run_logging(run_output_dir):
    """Configura el guardado de logs de la ejecución en fichero."""
    log_path = run_output_dir / "generation.log"
    log_file = open(log_path, "w", encoding="utf-8")

    sys.stdout = TeeStream(sys.__stdout__, log_file)
    sys.stderr = TeeStream(sys.__stderr__, log_file)

    return log_file, log_path


def main():
    """Función principal."""

    original_stdout = sys.stdout
    original_stderr = sys.stderr
    log_file = None
    
    # ============================================
    # CONFIGURACIÓN: Selecciona el método de generación
    # ============================================
    # Opciones disponibles:
    #   "dalle3"      - Genera imágenes nuevas sin usar la foto base (más creativo pero no mantiene rasgos)
    #   "gpt-image-1.5" - Edita la foto base con gpt-image-1.5 (mantiene mejor rasgos faciales)
    
    GENERATION_METHOD = "gpt-image-1.5"  # Cambia esto para usar otro método
    # ============================================
    
    try:
        # Crear directorio de salida para esta ejecución
        run_output_dir = create_run_output_dir(OUTPUT_DIR)

        # Activar guardado de logs en fichero (además de consola)
        log_file, log_path = setup_run_logging(run_output_dir)

        print(f"\nMétodo de generación seleccionado: {GENERATION_METHOD}")
        print(f"{'='*60}\n")
        print(f"Carpeta de generación actual: {run_output_dir.name}")
        print(f"Fichero de log: {log_path}\n")

        # Verificar que existe la carpeta de fotos
        if not FOTOS_DIR.exists():
            print(f"Error: La carpeta {FOTOS_DIR} no existe.")
            print("Por favor, crea la carpeta 'fotos' y añade las imágenes de los participantes.")
            return

        # Cargar personajes
        print("Cargando personajes...")
        characters = load_characters()
        print(f"Se cargaron {len(characters)} personajes.\n")

        # Seleccionar la función de generación según el método configurado
        if GENERATION_METHOD == "dalle3":
            generate_function = generate_character_image_dalle3
            method_label = "dalle3"
        elif GENERATION_METHOD == "gpt-image-1.5":
            generate_function = generate_character_image_gpt_image_15
            method_label = "gpt-image-1.5"
        else:
            print(f"Error: Método de generación '{GENERATION_METHOD}' no válido.")
            print("Opciones válidas: 'dalle3', 'gpt-image-1.5'")
            return

        # Procesar cada personaje
        success_count = 0
        for person_name, character_data in characters.items():
            print(f"\n{'='*60}")
            print(f"Procesando: {character_data['person_name']} -> {character_data['character_name']}")
            print(f"{'='*60}")

            # Buscar la foto correspondiente
            photo_path = find_matching_photo(person_name, FOTOS_DIR)

            if not photo_path:
                print(f"[ADVERTENCIA] No se encontro foto para {character_data['person_name']}")
                print(f"   Busca un archivo que contenga '{person_name}' en la carpeta fotos/")
                continue

            print(f"[OK] Foto encontrada: {photo_path.name}")

            # Generar imagen del personaje usando el método seleccionado
            image_base64 = generate_function(photo_path, character_data)

            if image_base64:
                # Guardar imagen con timestamp y método de generación
                timestamp = datetime.now().strftime("%d-%m-%Y--%H-%M")
                output_filename = f"{person_name}_{character_data['character_name'].replace(' ', '_').replace('/', '_')}_img_{method_label}_{timestamp}.png"
                output_path = run_output_dir / output_filename

                print(f"Guardando imagen...")
                if save_base64_image(image_base64, output_path):
                    print(f"[OK] Imagen guardada: {output_filename}")
                    success_count += 1
                else:
                    print(f"[ERROR] Error al guardar la imagen")
            else:
                print(f"[ERROR] Error al generar la imagen")

        print(f"\n{'='*60}")
        print(f"Proceso completado: {success_count}/{len(characters)} imágenes generadas")
        print(f"Las imágenes se guardaron en: {run_output_dir}")
        print(f"{'='*60}")

    finally:
        # Restaurar streams y cerrar fichero de log
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        if log_file is not None:
            log_file.close()


if __name__ == "__main__":
    main()
