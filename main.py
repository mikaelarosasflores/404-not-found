import os
import logging
import random
from dotenv import load_dotenv
import telebot

from utils import clean_key, downscale_if_needed, bytes_to_b64
from analyzers.vision import GroqVisionClient
from core.recommender import HelpDirectory
from core.classifier import classify_text  # <— REGLAS LOCALES (OCR)

# --- Cargar .env ---
load_dotenv(dotenv_path=os.path.join("bot", ".env"))
TELEGRAM_BOT_TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()
GROQ_API_KEY = clean_key(os.getenv("GROQ_API_KEY", ""))

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Falta TELEGRAM_BOT_TOKEN en bot/.env")
if not GROQ_API_KEY:
    raise ValueError("Falta GROQ_API_KEY en bot/.env")

# --- Init ---
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="Markdown")
vision = GroqVisionClient(GROQ_API_KEY, model="llama-3.2-90b-vision-preview")
helpdir = HelpDirectory()
user_country = {}
user_mode = {}  # modo_cuidado on/off

# ---------------- Empatía y tono humano ----------------
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

    line_alert = ""
    sev_norm = (severity or "desconocida").lower()
    if sev_norm in ("media", "alta"):
        line_alert = "\n⚠️ *Si hay riesgo o te sentís en peligro*, buscá ayuda inmediata: **911** (emergencias) o **144** (violencias de género, AR)."

    ev_text = "- " + ("\n- ".join(evidencias) if evidencias else "(sin evidencias)")
    rec_text = "- " + ("\n- ".join(recomendaciones) if recomendaciones else "(sin recomendaciones)")

    nota_texto = f"_Nota: {llm_note}_\n\n" if llm_note else ""

    msg = (
        f"🫶 *{intro}* {validation}\n\n"
        "🔎 *Análisis de imagen*\n\n"
        f"*Violencia detectada:* {'Sí' if detected else 'No (no concluyente)'}\n"
        f"*Categorías:* {', '.join(cats) if cats else '(ninguna)'}\n"
        f"*Severidad:* {severity}\n"
        f"*Evidencias:*\n{ev_text}\n\n"
        f"*Recomendaciones:*\n{rec_text}\n\n"
        f"📞 *Recursos de ayuda ({country}):*\n{recursos}"
        f"{line_alert}\n\n"
        "🔐 *Privacidad:* no guardo tus imágenes ni tus resultados. Podés borrar este chat cuando quieras.\n"
        f"{nota_texto}"
        f"{random.choice(EMP_CLOSINGS)}"
    )
    return msg

# --- Utils ---
def _download_file(file_id: str) -> bytes:
    info = bot.get_file(file_id)
    return bot.download_file(info.file_path)

def _pick_severity(a: str, b: str) -> str:
    order = {"baja": 1, "media": 2, "alta": 3, "desconocida": 0}
    sa, sb = order.get((a or "desconocida").lower(), 0), order.get((b or "desconocida").lower(), 0)
    return a if sa >= sb else b

def _process_image_bytes(msg, img_bytes: bytes):
    try:
        img_bytes = downscale_if_needed(img_bytes)
        b64 = bytes_to_b64(img_bytes)

        # 1) Intento con visión Groq (si falla, sigue)
        llm = vision.analyze_violence(b64) or {}
        llm_error = bool(llm.get("error"))  # cuando hay 403 u otro error

        # 2) Siempre intento OCR + reglas (mejora recall)
        ocr_text = vision.ocr_text(b64) or ""
        rule = classify_text(ocr_text) if ocr_text else {
            "detected": False, "categories": [], "severity": "desconocida", "evidence": [], "recommendations": []
        }

        # 3) Fusiono resultados (preferimos más severo y unimos categorías/evidencias)
        detected = bool(llm.get("detected") or rule.get("detected"))
        cats = list(dict.fromkeys((llm.get("categories") or []) + (rule.get("categories") or [])))
        severity = _pick_severity(llm.get("severity", "desconocida"), rule.get("severity", "desconocida"))
        evidencias = list(dict.fromkeys((llm.get("evidence") or []) + (rule.get("evidence") or [])))
        recomendaciones = list(dict.fromkeys((llm.get("recommendations") or []) + (rule.get("recommendations") or [])))

        # 4) Recursos según 1ra categoría útil
        country = user_country.get(msg.from_user.id, "AR")
        first_cat = (cats[0] if cats else "general")
        resources = helpdir.get(country, first_cat)

        # 5) Modo cuidado: recortar vocabulario fuerte
        if user_mode.get(msg.from_user.id, False) and evidencias:
            evidencias = [e for e in evidencias if len(e) <= 10]
            if "Hice un análisis simplificado por tu comodidad." not in recomendaciones:
                recomendaciones = ["Hice un análisis simplificado por tu comodidad."] + recomendaciones

        # 6) Mensaje empático
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

        # 7) Aviso de contenido sensible si el OCR vio insultos claros
        if any(w in (ocr_text.lower()) for w in ["mierda", "cerda", "sirvienta", "idiota", "inútil", "gorda"]):
            bot.send_message(msg.chat.id, "⚠️ Este contenido puede resultar sensible. Avisame si preferís que resuma sin mostrar frases textuales.")

        bot.reply_to(msg, text)

    except Exception as e:
        print("[ERR] _process_image_bytes:", repr(e))
        bot.reply_to(msg, "❌ Ocurrió un error al procesar la imagen. Probá de nuevo.")

# --- Comandos ---
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

# --- Imágenes ---
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

# --- Run ---
if __name__ == "__main__":
    print("🤖 Bot de descripción de imágenes iniciado…")
    print("📸 Esperando imágenes…")
    try:
        bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        print("[DBG] delete_webhook:", repr(e))
    bot.infinity_polling(timeout=10, long_polling_timeout=10)

# Agregado: mejora en el manejo de OCR y respuestas empáticas