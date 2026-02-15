"""Script para arreglar comillas tipográficas en JSON de forma robusta."""
import re

# Leer el archivo
with open('characters_with_objectives.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Procesar línea por línea
fixed_lines = []
for line in lines:
    # Reemplazar apóstrofes tipográficos
    line = line.replace(''', "'").replace(''', "'")
    
    # Para comillas dobles tipográficas, necesitamos ser más cuidadosos
    # Si la línea contiene "key": "value", necesitamos:
    # 1. Mantener las comillas de los delimitadores de key/value
    # 2. Escapar las comillas dentro de los valores
    
    # Buscar patrones como: "texto...": "valor con "comillas" aquí"
    # Estrategia: reemplazar todas las comillas tipográficas por normales primero
    # y luego escapar las que están dentro de valores
    
    # Contar comillas en la línea
    tipograficas = line.count('"') + line.count('"')
    
    if tipograficas > 0:
        # Hay comillas tipográficas
        # Reemplazarlas temporalmente con un marcador único
        line = line.replace('"', '<<<OPEN>>>').replace('"', '<<<CLOSE>>>')
        
        # Ahora procesar basándonos en la estructura JSON
        # Si la línea tiene el patrón "key": "value"
        # Las comillas <<<>>>que aparecen DESPUÉS del primer ":" son parte del valor y deben escaparse
        
        if '":' in line or '" :' in line:
            # Esta es una línea de key-value
            parts = line.split(':', 1)
            if len(parts) == 2:
                key_part = parts[0]
                value_part = parts[1]
                
                # En la parte del valor, reemplazar marcadores por comillas escapadas
                value_part = value_part.replace('<<<OPEN>>>', '\\"').replace('<<<CLOSE>>>', '\\"')
                
                # En la parte de la key, reemplazar marcadores por comillas normales
                key_part = key_part.replace('<<<OPEN>>>', '"').replace('<<<CLOSE>>>', '"')
                
                line = key_part + ':' + value_part
        else:
            # No es key-value, solo reemplazar por comillas normales
            line = line.replace('<<<OPEN>>>', '"').replace('<<<CLOSE>>>', '"')
    
    fixed_lines.append(line)

# Guardar
with open('characters_with_objectives.json', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("✓ Archivo procesado")

# Verificar
import json
try:
    with open('characters_with_objectives.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ JSON válido - {sum(len(chars) for chars in data.values())} personajes en {len(data)} líneas temporales")
except json.JSONDecodeError as e:
    print(f"✗ Error: {e}")
    print(f"   Línea {e.lineno}, columna {e.colno}")
