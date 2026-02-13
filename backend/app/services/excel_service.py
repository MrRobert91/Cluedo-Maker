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
            
            # Normalize column names to lowercase for flexibility
            df.columns = [c.lower().strip() for c in df.columns]
            
            participants = []
            for _, row in df.iterrows():
                # Flexible column matching
                name = row.get('nombre') or row.get('name') or row.get('participant')
                if not name or pd.isna(name):
                    continue
                
                participants.append({
                    "name": str(name).strip(),
                    "email": str(row.get('email', '')).strip() if 'email' in df.columns and not pd.isna(row['email']) else None,
                    "notes": str(row.get('notes', '')).strip() if 'notes' in df.columns and not pd.isna(row['notes']) else None
                })
                
            if not participants:
                raise HTTPException(status_code=400, detail="No valid participants found in the Excel file.")
                
            return participants
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing Excel file: {str(e)}")
