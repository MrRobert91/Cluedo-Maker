"""Script para arreglar las comillas tipográficas en el JSON."""
import json

# Leer el archivo como texto
with open('characters_with_objectives.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Estrategia: Reemplazar comillas tipográficas dentro de los valores por comillas escapadas
# Las comillas tipográficas que aparecen DENTRO de un string JSON deben escaparse

# Primero convertir apóstrofes
content = content.replace(''', "'")
content = content.replace(''', "'")

# Para las comillas dobles, necesitamos identificar si están:
# 1. Como delimitadores de keys/values (mantener como ")
# 2. Como parte del contenido (escapar como \")

# Enfoque simple: buscar y reemplazar manualmente los casos problemáticos
# Palabra "Dracarys" aparece con comillas
content = content.replace('"Dracarys"', '\\"Dracarys\\"')
content = content.replace('"yo solo vengo', '\\"yo solo vengo')
content = content.replace('zona VIP?"', 'zona VIP?\\"')
content = content.replace('"update"', '\\"update\\"')
content = content.replace('"edits"', '\\"edits\\"')
content = content.replace('"string"', '\\"string\\"')
content = content.replace('"no envejecimiento"', '\\"no envejecimiento\\"')

# Ahora reemplazar las comillas tipográficas restantes por comillas normales
content = content.replace('"', '"')
content = content.replace('"', '"')

# Guardar
with open('characters_with_objectives.json', 'w', encoding='utf-8') as f:
    f.write(content)

# Verificar que sea válido
try:
    with open('characters_with_objectives.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ JSON válido - {len(data)} líneas temporales procesadas")
except json.JSONDecodeError as e:
    print(f"✗ Error en JSON: {e}")

