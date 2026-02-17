import argparse
import io
import logging
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

try:
    from PIL import Image, ImageOps
except ImportError:
    Image = None
    ImageOps = None


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
PRESENTATION_SIZE = (1536, 1024)  # apaisado (landscape), aspect ratio 1536x1024


def setup_logger(output_pdf_path: Path) -> logging.Logger:
    """Configura logs en consola y fichero junto al PDF de salida."""
    logger = logging.getLogger("original_edited_pdf")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Limpiar handlers previos para evitar logs duplicados
    if logger.handlers:
        logger.handlers.clear()

    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    log_path = output_pdf_path.with_suffix(".log")

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%H:%M:%S")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Log file: %s", log_path)
    return logger


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFD", str(text))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text).strip()
    return text


def extract_character_name_from_title(title: str) -> str:
    return re.sub(r"\s*\([^)]+\)", "", title).strip()


def load_character_etiquetas(json_path: Path) -> Dict[str, str]:
    import json

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    etiquetas: Dict[str, str] = {}
    for _, chars in data.items():
        for char in chars:
            character_name = extract_character_name_from_title(char.get("titulo", ""))
            etiqueta = char.get("etiqueta", "")
            if character_name and etiqueta:
                etiquetas[normalize_text(character_name)] = etiqueta

    return etiquetas


def list_images(folder: Path) -> List[Path]:
    return sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS])


def person_from_original_filename(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"[_\- ]?foto$", "", stem, flags=re.IGNORECASE)
    return stem.strip()


def capitalize_first(text: str) -> str:
    if not text:
        return text
    return text[:1].upper() + text[1:]


def parse_edited_filename(path: Path) -> Tuple[str, str]:
    """
    Espera formato aproximado:
    {persona}_{personaje}_img_{metodo}_{fecha}.png
    """
    stem = path.stem

    if "_img_" in stem:
        left = stem.split("_img_", 1)[0]
    else:
        left = stem

    if "_" in left:
        person_part, character_part = left.split("_", 1)
    else:
        person_part, character_part = left, ""

    character_part = character_part.replace("_", " ").strip()
    return person_part.strip(), character_part


def build_latest_edited_map(edited_folder: Path) -> Dict[str, Tuple[Path, str]]:
    """Mapa por persona normalizada -> (ruta_imagen_editada, nombre_personaje)."""
    mapping: Dict[str, Tuple[Path, str]] = {}

    for img in list_images(edited_folder):
        person_raw, character_name = parse_edited_filename(img)
        key = normalize_text(person_raw)
        if not key:
            continue

        if key not in mapping:
            mapping[key] = (img, character_name)
        else:
            current_path, _ = mapping[key]
            if img.stat().st_mtime > current_path.stat().st_mtime:
                mapping[key] = (img, character_name)

    return mapping


def draw_image_fitted(c: canvas.Canvas, img_path: Path, x: float, y: float, max_w: float, max_h: float) -> None:
    # Respeta la orientación EXIF (evita fotos originales giradas)
    if Image is not None and ImageOps is not None:
        with Image.open(img_path) as pil_img:
            pil_img = ImageOps.exif_transpose(pil_img)
            buffer = io.BytesIO()
            pil_img.save(buffer, format="PNG")
            buffer.seek(0)
            reader = ImageReader(buffer)
    else:
        reader = ImageReader(str(img_path))

    iw, ih = reader.getSize()

    scale = min(max_w / iw, max_h / ih)
    draw_w = iw * scale
    draw_h = ih * scale

    dx = x + (max_w - draw_w) / 2
    dy = y + (max_h - draw_h) / 2

    c.drawImage(reader, dx, dy, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")


def draw_outlined_text(
    c: canvas.Canvas,
    x: float,
    y: float,
    text: str,
    *,
    font_name: str,
    font_size: int,
    fill_color=colors.white,
    stroke_color=colors.black,
) -> None:
    c.setLineWidth(max(1.5, font_size * 0.08))
    c.setFillColor(fill_color)
    c.setStrokeColor(stroke_color)

    t = c.beginText()
    t.setTextOrigin(x, y)
    t.setFont(font_name, font_size)
    t.setTextRenderMode(2)  # fill + stroke
    t.textLine(text)
    c.drawText(t)


def draw_page(c: canvas.Canvas, image_path: Path, top_text: str, bottom_text: Optional[str] = None) -> None:
    page_w, page_h = c._pagesize

    text_margin = 24
    top_text_y = page_h - 88
    subtitle_y = page_h - 160

    draw_outlined_text(
        c,
        text_margin,
        top_text_y,
        top_text,
        font_name="Helvetica-Bold",
        font_size=72,
    )

    if bottom_text:
        draw_outlined_text(
            c,
            text_margin,
            subtitle_y,
            bottom_text,
            font_name="Helvetica-Bold",
            font_size=48,
        )

    # Imagen a sangre: ocupa todo el lienzo del PDF sin márgenes manuales.
    # Solo quedarán bandas si es necesario para NO deformar (preserveAspectRatio=True).
    draw_image_fitted(c, image_path, 0, 0, page_w, page_h)

    # Re-dibujar textos encima para asegurar visibilidad sobre la imagen
    draw_outlined_text(
        c,
        text_margin,
        top_text_y,
        top_text,
        font_name="Helvetica-Bold",
        font_size=72,
    )

    if bottom_text:
        draw_outlined_text(
            c,
            text_margin,
            subtitle_y,
            bottom_text,
            font_name="Helvetica-Bold",
            font_size=48,
        )
    c.showPage()


def create_original_vs_edited_pdf(
    original_images_dir: Path,
    edited_images_dir: Path,
    characters_objectives_json: Path,
    output_pdf_path: Path,
    logger: Optional[logging.Logger] = None,
) -> None:
    logger = logger or logging.getLogger("original_edited_pdf")

    logger.info("Iniciando generación de PDF")
    logger.info("Originales: %s", original_images_dir)
    logger.info("Editadas: %s", edited_images_dir)
    logger.info("JSON personajes: %s", characters_objectives_json)
    logger.info("Salida PDF: %s", output_pdf_path)

    etiquetas = load_character_etiquetas(characters_objectives_json)
    originals = list_images(original_images_dir)
    edited_map = build_latest_edited_map(edited_images_dir)

    logger.info("Imágenes originales encontradas: %d", len(originals))
    logger.info("Imágenes editadas indexadas por persona: %d", len(edited_map))

    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_pdf_path), pagesize=PRESENTATION_SIZE)

    for idx, original in enumerate(originals, start=1):
        person_raw = person_from_original_filename(original)
        person_display = capitalize_first(person_raw)
        person_key = normalize_text(person_raw)

        logger.info("[%d/%d] Procesando persona: %s", idx, len(originals), person_display)

        # Página 1: original
        draw_page(c, original, f"{person_display} es...")

        # Página 2: editada (si existe)
        edited_info = edited_map.get(person_key)
        if edited_info:
            edited_path, character_name = edited_info
            etiqueta = etiquetas.get(normalize_text(character_name), "")
            logger.info("  -> Editada encontrada: %s", edited_path.name)
            draw_page(c, edited_path, character_name or person_raw, etiqueta)
        else:
            logger.warning("  -> No se encontró imagen editada para: %s", person_display)
            # Si no existe editada, añadimos una diapositiva informativa para mantener la secuencia
            page_w, page_h = c._pagesize
            draw_outlined_text(
                c,
                36,
                page_h - 88,
                person_display,
                font_name="Helvetica-Bold",
                font_size=72,
            )
            draw_outlined_text(
                c,
                36,
                page_h - 160,
                "No se encontró imagen editada para esta persona.",
                font_name="Helvetica-Bold",
                font_size=48,
            )
            c.showPage()

    c.save()
    logger.info("PDF generado correctamente: %s", output_pdf_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Crear PDF alternando imagen original y editada por personaje")
    parser.add_argument("--originals", required=True, help="Carpeta de imágenes originales")
    parser.add_argument("--edited", required=True, help="Carpeta de imágenes editadas")
    parser.add_argument("--json", required=True, help="Ruta a characters_with_objectives.json")
    parser.add_argument("--output", required=True, help="Ruta del PDF de salida")
    args = parser.parse_args()

    output_pdf = Path(args.output)
    logger = setup_logger(output_pdf)

    create_original_vs_edited_pdf(
        original_images_dir=Path(args.originals),
        edited_images_dir=Path(args.edited),
        characters_objectives_json=Path(args.json),
        output_pdf_path=output_pdf,
        logger=logger,
    )


if __name__ == "__main__":
    main()
