import os
import base64
from io import BytesIO

# --- imports opcionales (no romper si faltan) ---
try:
    import cv2  # type: ignore
    import numpy as np  # type: ignore
    _CV_OK = True
except Exception:
    cv2 = None
    np = None
    _CV_OK = False

from PIL import Image
import pytesseract

# === Windows: decirle explícitamente dónde está tesseract.exe ===
# Cambiá esta ruta si tu instalación es distinta.
if os.name == "nt":
    default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.isfile(default_path):
        pytesseract.pytesseract.tesseract_cmd = default_path
    # Si lo instalaste en otro lado, poné esa ruta arriba.

# === Si instalaste el idioma español (spa.traineddata) en otra carpeta,
#     podés fijar TESSDATA_PREFIX:
# os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# ------------------------------------------------------
# 🔧 UTILIDADES
# ------------------------------------------------------

def _decode_b64_to_cv2(b64_str: str):
    if not _CV_OK:
        return None
    try:
        img_data = base64.b64decode(b64_str)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print("[ERR] _decode_b64_to_cv2:", e)
        return None

def _downscale_if_needed(image_bytes: bytes, max_side: int = 1600) -> bytes:
    try:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        w, h = img.size
        scale = max(w, h) / max_side
        if scale > 1:
            new_w, new_h = int(w / scale), int(h / scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)
        out = BytesIO()
        img.save(out, format="JPEG", quality=90)
        return out.getvalue()
    except Exception as e:
        print("[ERR] downscale_if_needed:", e)
        return image_bytes

# ------------------------------------------------------
# 🧠 CLIENTE DE VISIÓN
# ------------------------------------------------------

class GroqVisionClient:
    """
    Cliente de visión. Si no hay permiso para LLM/visión, usa OCR local + reglas.
    """

    def __init__(self, api_key: str, model: str = "llama-3.2-90b-vision-preview"):
        self.api_key = api_key
        self.model = model

    # ---------- OCR embebido en la clase ----------
    def ocr_text(self, b64: str) -> str:
        """
        Extrae texto de una imagen (base64) usando OCR optimizado
        con preprocesamiento y Tesseract en español + inglés.
        """
        txt = ""
        # Si hay OpenCV, preprocesamos fuerte
        if _CV_OK:
            img = _decode_b64_to_cv2(b64)
            if img is None:
                return ""
            h, w = img.shape[:2]

            # Subir resolución si la imagen es pequeña
            if max(h, w) < 1200:
                scale = 1200 / max(h, w)
                img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

            # Escala de grises + reducción de ruido
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.fastNlMeansDenoising(gray, h=15)

            # Aumentar contraste + binarización
            gray = cv2.convertScaleAbs(gray, alpha=1.6, beta=8)
            _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

            config = "--oem 3 --psm 6 -l spa+eng"
            try:
                txt = pytesseract.image_to_string(bw, config=config) or ""
            except Exception as e:
                print("[ERR] pytesseract:", e)
                txt = ""
        else:
            # Fallback sin OpenCV: usar PIL directo
            try:
                img_data = base64.b64decode(b64)
                pil = Image.open(BytesIO(img_data)).convert("L")
                config = "--oem 3 --psm 6 -l spa+eng"
                txt = pytesseract.image_to_string(pil, config=config) or ""
            except Exception as e:
                print("[ERR] pytesseract (PIL fallback):", e)
                txt = ""

        return txt.strip()

    def analyze_violence(self, b64_img: str) -> dict:
        """
        Analiza una imagen y devuelve detección de violencia con OCR + reglas locales.
        (Si más adelante habilitás visión LLM, podés fusionar ambos resultados.)
        """
        text = self.ocr_text(b64_img)

        if not text:
            return {
                "detected": False,
                "categories": [],
                "severity": "desconocida",
                "evidence": [],
                "recommendations": [],
            }

        t = text.lower()

        # Listas simples (podés expandirlas)
        insultos = ["idiota", "inútil", "cerda", "mierda", "mentirosa", "estúpida", "fea", "callate"]
        manipulacion = [
            "sin mí no sos nada", "todo es tu culpa", "nadie te va a creer",
            "me hacés enojar", "si me quisieras", "me obligás"
        ]
        amenazas = [
            "vas a ver", "te voy a", "te voy a denunciar", "me las vas a pagar",
            "no sabés con quién te metés"
        ]

        evid = []
        for kw in insultos + manipulacion + amenazas:
            if kw in t:
                evid.append(kw)

        score = 0
        score += 1 * sum(k in t for k in insultos)
        score += 2 * sum(k in t for k in manipulacion)
        score += 3 * sum(k in t for k in amenazas)

        if score >= 4:
            sev = "alta"
        elif score >= 2:
            sev = "media"
        elif score >= 1:
            sev = "baja"
        else:
            sev = "desconocida"

        cats = ["verbal"] if evid else []

        recs = []
        if sev in ("media", "alta"):
            recs = [
                "No respondas a las agresiones; guardá evidencia (capturas).",
                "Bloqueá/silenciá a la persona agresora en la plataforma.",
                "Contale a alguien de confianza y buscá apoyo."
            ]

        return {
            "detected": bool(evid),
            "categories": cats,
            "severity": sev,
            "evidence": evid,
            "recommendations": recs
        }
