import pandas as pd
from typing import List, Dict, Any
from fastapi import UploadFile, HTTPException
import io

class ExcelParsingService:
    @staticmethod
    async def parse_participants(file: UploadFile) -> List[Dict[str, Any]]:
        """
        Parses an uploaded Excel file to extract participant data.
        Expected columns: Name, Email (optional), Notes (optional)
        """
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")
        
        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            
            # Map specific columns from the provided Excel format
            # Using a mapping dictionary for clarity
            col_map = {
                "nombre": "name",
                "correo electrónico": "email",
                "número de teléfono (solo para emergencias de guion, el contacto será por correo)": "phone",
                "sube una foto tuya (para tu ficha oficial de sospechoso, que se te vea claramente la cara y estés solo/a)  porfi, ¡¡¡¡¡nombra la foto con tu nombre!!!!!": "photo_url",
                "¿te apetece meterte en personaje e interpretar un poco?": "is_improviser",
                "¿qué tono te gustaría para el cluedo del cumpleaños de elena?": "tone_preference",
                "¿qué tipo de pruebas te gustan más? (elige varias)": "test_preference",
                "¿te gustaría tener objetivos secretos propios durante el juego?": "wants_secret_objectives",
                "nivel de implicación en el disfraz": "costume_level",
                "¿qué ambientaciones te apetecen más? (elige varias si quieres)": "setting_preference",
                "¿hay algo que te incomode o prefieres evitar en el juego?": "avoid_topics",
                "¿qué te haría especial ilusión que incluyéramos?": "special_requests",
                "¿hay algo más que quieras contarme (sugerencias, avisos, ideas, confesiones espontáneas o cualquier cosa que deba saber)?": "additional_info",
                "¿estás 100% seguro/a de que vas a venir al cluedo del cumpleaños de elena?": "attendance_confirmed"
            }
            
            # Normalize df columns to lower, stripped, and remove extra spaces within
            # A helper to fuzzy match or just use simple normalization might be safer given the long names
            # Let's clean the DF columns first
            df.columns = [str(c).lower().strip().replace("  ", " ") for c in df.columns]

            participants = []
            for _, row in df.iterrows():
                # Name is mandatory
                # We try to find the 'nombre' column. The exact string from valid_columns might differ slightly due to spaces.
                # Let's find the column that *contains* "nombre" if exact match fails, or rely on index if consistent.
                # Given the user input, we'll try strict mapping first but allow for some flexibility.
                
                # Check for "nombre" column
                name_col = next((c for c in df.columns if "nombre" in c and "foto" not in c), None)
                if not name_col:
                     # Fallback to first column? No, risky. 
                     continue
                
                name = row[name_col]
                if pd.isna(name):
                    continue

                p_data = {"name": str(name).strip()}
                
                # Helper to get value securely
                def get_val(key_fragment):
                    col = next((c for c in df.columns if key_fragment in c), None)
                    if col and not pd.isna(row[col]):
                        return str(row[col]).strip()
                    return None

                p_data["email"] = get_val("correo electrónico")
                p_data["phone"] = get_val("número de teléfono")
                p_data["photo_url"] = get_val("sube una foto")
                p_data["is_improviser"] = get_val("meterte en personaje")
                p_data["tone_preference"] = get_val("qué tono te gustaría")
                p_data["test_preference"] = get_val("qué tipo de pruebas")
                p_data["wants_secret_objectives"] = get_val("objetivos secretos")
                p_data["costume_level"] = get_val("nivel de implicación")
                p_data["setting_preference"] = get_val("qué ambientaciones")
                p_data["avoid_topics"] = get_val("algo que te incomode")
                p_data["special_requests"] = get_val("especial ilusión")
                p_data["additional_info"] = get_val("algo más que quieras contarme")
                p_data["attendance_confirmed"] = get_val("seguro/a de que vas a venir")
                
                participants.append(p_data)
                
            if not participants:
                raise HTTPException(status_code=400, detail="No valid participants found in the Excel file.")
                
            return participants
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing Excel file: {str(e)}")
