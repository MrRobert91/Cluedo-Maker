# Generador de Fotos de Personajes

Este script transforma las fotos reales de los participantes en imágenes de sus personajes asignados usando la API de OpenAI.

## Configuración

### 1. Instalar dependencias

```bash
pip install openai
```

### 2. Configurar API Key de OpenAI

Tienes dos opciones:

**Opción A: Variable de entorno (recomendado)**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="tu-api-key-aqui"

# Windows CMD
set OPENAI_API_KEY=tu-api-key-aqui

# Linux/Mac
export OPENAI_API_KEY="tu-api-key-aqui"
```

**Opción B: Editar el script**
Abre `generate_character_photos.py` y modifica la línea:
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "tu-api-key-aqui")
```

### 3. Preparar las fotos

1. Coloca las fotos de los participantes en la carpeta `experiments/fotos/`
2. Nombra cada foto con el nombre de la persona (ej: `Susana.jpg`, `Arturo.png`, etc.)
3. Formatos soportados: JPG, JPEG, PNG

**Ejemplo de estructura:**
```
experiments/
  ├── fotos/
  │   ├── Susana.jpg
  │   ├── Arturo.png
  │   ├── Beatriz.jpg
  │   └── ...
  ├── generate_character_photos.py
  └── characters_with_objectives.json
```

## Uso

Ejecuta el script:

```bash
cd backend/experiments
python generate_character_photos.py
```

## Resultado

El script:
1. Lee cada foto de la carpeta `fotos/`
2. Identifica a qué personaje corresponde según el JSON
3. Usa la API de **Image Edit** con el modelo **GPT Image 1.5** para transformar la foto
4. Utiliza `input_fidelity="low"` y `quality="low"` para permitir más libertad creativa en la transformación
5. Guarda las imágenes generadas en `experiments/fotos_personajes/`

Las imágenes generadas se nombran como:
`{NombrePersona}_{NombrePersonaje}.png`

Ejemplo: `Susana_Daenerys.png`

## Notas

- **Usa GPT Image 1.5**, el modelo más avanzado de OpenAI para edición de imágenes
- **Input Fidelity "Low"** permite más libertad creativa en la transformación
- **Quality "Low"** renderizado estándar, más rápido
- **Moderation "Low"** permite mayor libertad creativa en los resultados
- Cada generación consume créditos de la API de OpenAI
- El proceso puede tardar varios minutos dependiendo del número de participantes
- Las imágenes se generan en formato PNG 1024x1024 píxeles
- Acepta cualquier formato de foto de entrada (JPG, PNG, etc.)

## Solución de problemas

**"No se encontró foto para X"**
- Verifica que el nombre del archivo contenga el nombre de la persona
- El script busca coincidencias parciales (no hace falta que sea exacto)

**"Error al generar imagen"**
- Verifica tu API key de OpenAI
- Asegúrate de tener créditos disponibles
- Comprueba tu conexión a internet
La API de Image Edit (DALL-E 2) trabaja mejor con fotos claras y bien iluminadas
- Asegúrate de que la cara esté centrada en la foto original
- Puedes ajustar el prompt en la función `generate_character_prompt()` para dar más énfasis a mantener rasgos faciales

**Limitaciones de DALL-E 2 Image Edit**
- El prompt debe ser conciso (máximo 1000 caracteres)
- Las imágenes deben ser PNG y cuadradas
- El modelo mantiene los rasgos faciales pero puede variar el estilo significativamente
- GPT-4 Vision puede tener limitaciones para capturar todos los rasgos
- Puedes ajustar el prompt en la función `generate_character_prompt()`
