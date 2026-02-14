import json
import os
import sys

# Add the current directory to path to import from sibling
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from generate_character_sheets import chars
except ImportError:
    print("Error: Could not import chars from generate_character_sheets.py")
    sys.exit(1)

def extract_to_json():
    # Group by faction
    factions_data = {}
    
    for char in chars:
        faction = char["faccion"]
        if faction not in factions_data:
            factions_data[faction] = []
            
        factions_data[faction].append({
            "titulo": char["titulo"],
            "etiqueta": char["etiqueta"],
            "bio": char["bio"],
            "como_es": char["como_es"],
            "disfraz": char["disfraz"]
        })
    
    output_path = os.path.join(os.path.dirname(__file__), "characters_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(factions_data, f, ensure_ascii=False, indent=4)
    
    print(f"OK: Datos de {len(chars)} personajes exportados a {output_path}")

if __name__ == "__main__":
    extract_to_json()
