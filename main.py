import os
import logging
import random
import base64
from io import BytesIO

from dotenv import load_dotenv
import telebot

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

# ------------------------------------------------------
#  Cargar variables de entorno (.env en la raíz)
# ------------------------------------------------------
load_dotenv() 

# ------------------------------------------------------
#  UTILIDADES BÁSICAS (reemplazan utils.*)
# ------------------------------------------------------
def clean_key(key: str | None) -> str:
    """Limpia la API key (antes venía de utils.clean_key)."""
    return (key or "").strip()

def bytes_to_b64(data: bytes) -> str:
    """Convierte bytes de imagen a base64 (antes venía de utils.bytes_to_b64)."""
    return base64.b64encode(data).decode("utf-8")

def downscale_if_needed(image_bytes: bytes, max_side: int = 1600) -> bytes:
    """
    Reduce el tamaño de la imagen si es muy grande.
    Equivalente a utils.downscale_if_needed pero local a este archivo.
    """
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

# ------------------------------------------------------
#  Directorio de ayuda simple (reemplaza HelpDirectory)
# ------------------------------------------------------
from dataclasses import dataclass
from typing import List

@dataclass
class HelpResource:
    title: str
    contact: str
    note: str | None = None

class HelpDirectory:
    """
    Versión simplificada embebida en este archivo.
    Podés ajustar contactos o agregar más países/categorías.
    """
    def __init__(self):
        self.data = {
            "AR": {
                "general": [
                    HelpResource("Línea 144", "144", "Atención a personas en situación de violencia por motivos de género."),
                    HelpResource("Emergencias", "911", "Si hay riesgo inmediato."),
                ],
                "verbal": [
                    HelpResource("Línea 144", "144", "Podés pedir orientación sobre violencia psicológica o verbal.")
                ],
            }
        }

    def get(self, country: str, category: str) -> List[HelpResource]:
        country = (country or "AR").upper()
        cat = category or "general"
        by_country = self.data.get(country, self.data["AR"])
        return by_country.get(cat, by_country.get("general", []))

# ------------------------------------------------------
#  Configuración de Tesseract
# ------------------------------------------------------
if os.name == "nt":
    default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.isfile(default_path):
        pytesseract.pytesseract.tesseract_cmd = default_path

    # Si lo instalaste en otro lado, cambiá la ruta de arriba.

# ------------------------------------------------------
#  CLIENTE DE VISIÓN
# ------------------------------------------------------
class GroqVisionClient:
    """
    Cliente de visión local: usa sólo OCR + reglas para detectar violencia.
    (Si luego habilitan Groq visión, acá se puede integrar el LLM.)
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

# ------------------------------------------------------
#  Frases empáticas
# ------------------------------------------------------
EMP_INTROS_DETECTED = [
    "Gracias por confiar en mí y compartir esta imagen. Siento que estés pasando por algo así.",
    "Lamento que estés lidiando con esto. No estás sola/solo: estoy para ayudarte.",
    "Gracias por enviarla. Lo que muestra puede ser difícil de ver; acá va un análisis con cuidado."
]

EMP_INTROS_UNCLEAR = [
    "Gracias por compartir la imagen. Haré un análisis cuidadoso.",
    "Gracias por enviarla; voy a revisar lo que se alcanza a leer con mucha cautela.",
    "Recibí la imagen. Te comparto una lectura preliminar."
]

EMP_VALIDATIONS = [
    "Lo que sentís es válido.",
    "Pedir ayuda es un acto de fortaleza.",
    "No es tu culpa.",
]

EMP_CLOSINGS = [
    "Si querés, puedo buscar más recursos o pensar juntas/os próximos pasos.",
    "Podés escribirme cuando lo necesites; avanzo a tu ritmo.",
    "Si preferís, mantengo el análisis breve y sin detalles; decime cómo te sentís más cómoda/o.",
]

def _compose_empathetic_message(
    detected: bool,
    cats: list[str],
    severity: str,
    evidencias: list[str],
    recomendaciones: list[str],
    country: str,
    recursos: str,
    llm_note: str | None = None
) -> str:
    intro = random.choice(EMP_INTROS_DETECTED if detected else EMP_INTROS_UNCLEAR)
    validation = random.choice(EMP_VALIDATIONS)

    sev_norm = (severity or "desconocida").lower()

    # Explicación del nivel de severidad
    if sev_norm == "alta":
        sev_expl = (
            "Se detectan varias frases agresivas y/o amenazas, lo que sugiere un nivel de violencia significativo "
            "y un posible impacto fuerte en lo emocional."
        )
    elif sev_norm == "media":
        sev_expl = (
            "Se identifican expresiones agresivas o manipuladoras que pueden afectar tu bienestar, "
            "aunque no sean amenazas directas."
        )
    elif sev_norm == "baja":
        sev_expl = (
            "Se encontraron indicios de lenguaje hiriente o descalificador, pero con menor intensidad o frecuencia."
        )
    else:
        sev_expl = (
            "No se encontraron suficientes señales claras como para estimar con precisión el nivel de violencia."
        )

    # Resumen de evidencias / contador de frases agresivas
    evid_count = len(evidencias)
    if evid_count > 0:
        ejemplos = ", ".join(f"“{e}”" for e in evidencias[:4])
        evid_resumen = (
            f"Se detectaron *{evid_count}* frases o expresiones potencialmente agresivas.\n"
            f"Algunos ejemplos: {ejemplos}."
        )
    else:
        evid_resumen = (
            "No se identificaron frases explícitamente agresivas en el texto extraído; "
            "aun así, si algo de lo que ves o sentís te incomoda, tu percepción es importante."
        )

    line_alert = ""
    if sev_norm in ("media", "alta"):
        line_alert = (
            "\n⚠️ *Si hay riesgo o te sentís en peligro*, buscá ayuda inmediata: "
            "**911** (emergencias) o **144** (violencias de género, AR)."
        )

    ev_text = "- " + ("\n- ".join(evidencias) if evidencias else "(sin evidencias listadas)")
    rec_text = "- " + ("\n- ".join(recomendaciones) if recomendaciones else "(sin recomendaciones específicas)")

    nota_texto = f"_Nota: {llm_note}_\n\n" if llm_note else ""

    msg = (
        f"🫶 *{intro}* {validation}\n\n"
        "🔎 *Análisis de imagen*\n\n"
        f"*Violencia detectada:* {'Sí' if detected else 'No (no concluyente)'}\n"
        f"*Categorías:* {', '.join(cats) if cats else '(ninguna)'}\n"
        f"*Severidad:* {severity}\n"
        f"_Motivo de esta severidad:_ {sev_expl}\n\n"
        f"📌 *Resumen de frases detectadas:*\n{evid_resumen}\n\n"
        f"*Evidencias (detalle):*\n{ev_text}\n\n"
        f"*Recomendaciones:*\n{rec_text}\n\n"
        f"📞 *Recursos de ayuda ({country}):*\n{recursos}"
        f"{line_alert}\n\n"
        "🔐 *Privacidad:* no guardo tus imágenes ni tus resultados. Podés borrar este chat cuando quieras.\n"
        f"{nota_texto}"
        f"{random.choice(EMP_CLOSINGS)}"
    )
    return msg

# ------------------------------------------------------
#  Configuración del bot de Telegram
# ------------------------------------------------------
TELEGRAM_BOT_TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()
GROQ_API_KEY = clean_key(os.getenv("GROQ_API_KEY", ""))

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Falta TELEGRAM_BOT_TOKEN en .env")
if not GROQ_API_KEY:
    raise ValueError("Falta GROQ_API_KEY en .env")

telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="Markdown")
vision = GroqVisionClient(GROQ_API_KEY, model="llama-3.2-90b-vision-preview")
helpdir = HelpDirectory()
user_country: dict[int, str] = {}
user_mode: dict[int, bool] = {}  # modo_cuidado on/off

# ------------------------------------------------------
# Funciones auxiliares
# ------------------------------------------------------
def _download_file(file_id: str) -> bytes:
    info = bot.get_file(file_id)
    return bot.download_file(info.file_path)

def _process_image_bytes(msg, img_bytes: bytes):
    try:
        # ---------- 1) Chequear tamaño mínimo ----------
        try:
            pil_img = Image.open(BytesIO(img_bytes))
            w, h = pil_img.size
        except Exception:
            w, h = 0, 0

        # si la imagen es muy chiquita, avisamos y salimos
        if w and h and (w < 300 or h < 500):
            print(f"[DBG] Tamaño imagen: {w}x{h}")
            bot.reply_to(
                msg,
                "🔎 La imagen que enviaste es muy pequeña y no se alcanzan a distinguir bien las letras.\n\n"
                "📌 *Recomendación:*\n"
                "• Enviá una captura donde el texto ocupe buena parte de la pantalla.\n"
                "• Idealmente que tenga al menos ~600×600 píxeles o más.\n"
                "• Evitá fotos muy lejos, movidas o borrosas."
            )
            return

        # ---------- 2) Redimensionar y pasar a base64 ----------
        img_bytes = downscale_if_needed(img_bytes)
        b64 = bytes_to_b64(img_bytes)

        # ---------- 3) OCR rápido para ver si se leyó algo ----------
        ocr_preview = vision.ocr_text(b64) or ""
        clean_text = ocr_preview.strip()

        # Caso 1: no hay texto en absoluto
        if not clean_text:
            bot.reply_to(
                msg,
                "👀 No detecté texto en la imagen que enviaste.\n\n"
                "Este bot está pensado para analizar *capturas de chats o textos escritos* para detectar posibles violencias.\n\n"
                "📌 *Recomendación:*\n"
                "• Enviá una captura donde se vea texto (por ejemplo, mensajes de chat, publicaciones o comentarios).\n"
                "• Si es una foto sin texto, no voy a poder hacer análisis de violencia verbal."
            )
            return

        # Caso 2: hay texto, pero muy poquito → probablemente borroso / ilegible
        if len(clean_text) < 15:
            bot.reply_to(
                msg,
                "😕 No pude leer claramente el texto de la imagen, parece poco nítida o borrosa.\n\n"
                "📌 *Para que pueda ayudarte mejor:*\n"
                "• Enviá una captura donde las letras se vean nítidas.\n"
                "• Evitá hacerle foto a otra pantalla desde muy lejos.\n"
                "• Si podés, hacé zoom al chat antes de sacar la captura."
            )
            return

        # ---------- 4) Análisis normal de violencia ----------
        llm = vision.analyze_violence(b64) or {}
        llm_error = bool(llm.get("error"))  # hoy siempre False, pero se mantiene

        detected = bool(llm.get("detected"))
        cats = llm.get("categories") or []
        severity = llm.get("severity", "desconocida")
        evidencias = llm.get("evidence") or []
        recomendaciones = llm.get("recommendations") or []

        country = user_country.get(msg.from_user.id, "AR")
        first_cat = (cats[0] if cats else "general")
        resources = helpdir.get(country, first_cat)

        if user_mode.get(msg.from_user.id, False) and evidencias:
            evidencias = [e for e in evidencias if len(e) <= 10]
            if "Hice un análisis simplificado por tu comodidad." not in recomendaciones:
                recomendaciones = ["Hice un análisis simplificado por tu comodidad."] + recomendaciones

        llm_note = "análisis LLM no disponible (se usó OCR + reglas locales)." if llm_error else None
        text = _compose_empathetic_message(
            detected=detected,
            cats=cats,
            severity=severity,
            evidencias=evidencias,
            recomendaciones=recomendaciones,
            country=country,
            recursos="\n".join([f"- {r.title}: {r.contact}" + (f' — {r.note}' if r.note else '') for r in resources]),
            llm_note=llm_note
        )

        lower_evid = " ".join(evidencias).lower()
        if any(w in lower_evid for w in ["mierda", "cerda", "sirvienta", "idiota", "inútil", "gorda"]):
            bot.send_message(
                msg.chat.id,
                "⚠️ Este contenido puede resultar sensible. Avisame si preferís que resuma sin mostrar frases textuales."
            )

        bot.reply_to(msg, text)

    except Exception as e:
        print("[ERR] _process_image_bytes:", repr(e))
        bot.reply_to(msg, "❌ Ocurrió un error al procesar la imagen. Probá de nuevo.")

# ------------------------------------------------------
# Handlers de comandos
# ------------------------------------------------------
@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(
        msg,
        "👋 ¡Hola! Soy *Eva SafeBot*, un asistente que analiza *imágenes* para detectar posibles *violencias* o manipulaciones.\n\n"
        "📸 Enviame una captura o imagen.\n"
        "🌎 Configurá tu país con `/setcountry AR`.\n"
        "💗 Activá el modo cuidado con `/modo_cuidado on`.\n"
        "ℹ️ Más info: /help"
    )

@bot.message_handler(commands=["help"])
def help_(msg):
    bot.reply_to(
        msg,
        "1️⃣ Enviá una imagen (chat, publicación, etc.).\n"
        "2️⃣ Detecto texto con OCR y analizo posibles agresiones o manipulación.\n"
        "3️⃣ Te devuelvo categorías, severidad, evidencias y recursos útiles.\n"
        "⚠️ No es un diagnóstico ni reemplaza acompañamiento profesional."
    )

@bot.message_handler(commands=["setcountry"])
def set_country(msg):
    parts = (msg.text or "").strip().split()
    if len(parts) == 2 and parts[1].isalpha() and len(parts[1]) == 2:
        iso = parts[1].upper()
        user_country[msg.from_user.id] = iso
        bot.reply_to(msg, f"🌎 País configurado: *{iso}*")
    else:
        bot.reply_to(msg, "Usa: `/setcountry AR` (código ISO-2).")

@bot.message_handler(commands=["modo_cuidado"])
def toggle_mode(msg):
    parts = (msg.text or "").split()
    if len(parts) == 2 and parts[1].lower() in ["on", "off"]:
        state = parts[1].lower() == "on"
        user_mode[msg.from_user.id] = state
        bot.reply_to(msg, f"💗 *Modo cuidado {'activado' if state else 'desactivado'}.*")
    else:
        bot.reply_to(msg, "Usá `/modo_cuidado on` o `/modo_cuidado off`.")

@bot.message_handler(commands=["ping"])
def ping(msg):
    bot.reply_to(msg, "🏓 pong")

# ------------------------------------------------------
# Handlers de imágenes
# ------------------------------------------------------
@bot.message_handler(content_types=["photo"])
def analyze_photo(msg):
    bot.reply_to(msg, "📸 Imagen recibida. Analizando… ⏳")
    try:
        photo = msg.photo[-1]
        img_bytes = _download_file(photo.file_id)
        _process_image_bytes(msg, img_bytes)
    except Exception as e:
        print("[ERR] analyze_photo:", repr(e))
        bot.reply_to(msg, "❌ Error al procesar la imagen.")

@bot.message_handler(content_types=["document"])
def analyze_document(msg):
    doc = msg.document
    if not doc or not (doc.mime_type or "").startswith("image/"):
        return
    bot.reply_to(msg, "🖼️ Imagen (archivo) recibida. Analizando… ⏳")
    try:
        img_bytes = _download_file(doc.file_id)
        _process_image_bytes(msg, img_bytes)
    except Exception as e:
        print("[ERR] analyze_document:", repr(e))
        bot.reply_to(msg, "❌ Error al procesar la imagen.")

# ------------------------------------------------------
# Run
# ------------------------------------------------------
if __name__ == "__main__":
    print("🤖 Bot de análisis de imágenes iniciado…")
    print("📸 Esperando imágenes…")
    try:
        bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        print("[DBG] delete_webhook:", repr(e))
    bot.infinity_polling(timeout=10, long_polling_timeout=10)
