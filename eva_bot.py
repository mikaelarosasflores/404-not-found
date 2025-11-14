import os, sys, json
from typing import Dict, Any
from dotenv import load_dotenv
from groq import Groq
import telebot as tlb

# rutas base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# módulos locales
from analyzers.sentiment_analyzer import SentimentAnalyzer
from analyzers.voice_analyzer import VoiceAnalyzer
from analyzers.image_analyzer import ImageAnalyzer
from data.system_prompt import build_eva_prompt

# ---------------------- ENV ----------------------
load_dotenv()
GROQ_API_KEY       = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL         = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
DATASET_PATH       = os.path.join(DATA_DIR, "dataset.json")

if not GROQ_API_KEY or not TELEGRAM_BOT_TOKEN:
    print("Falta GROQ_API_KEY o TELEGRAM_TOKEN en .env")
    sys.exit(1)

# ---------------------- INIT ----------------------
groq = Groq(api_key=GROQ_API_KEY)
bot = tlb.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")
sa = SentimentAnalyzer()

# saludo por chat (solo una vez)
_seen_chats: Dict[int, bool] = {}

# ---------------------- DATASET ----------------------
def load_dataset(path: str) -> Dict[str, Any]:
    abspath = path if os.path.isabs(path) else os.path.join(BASE_DIR, path)
    try:
        with open(abspath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"[dataset] error leyendo {abspath}: {e}")
        return {}

DATASET = load_dataset(DATASET_PATH)

# ---------------------- LLM ----------------------
def ask_llm(messages, temperature=0.15, max_tokens=180) -> str:
    resp = groq.chat.completions.create(
        model=GROQ_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=messages,
    )
    return (resp.choices[0].message.content or "").strip()

def generate_reply(user_text: str, analysis: Dict[str, Any], input_type: str, chat_id: int) -> str:
    # flags de estilo
    intro = not _seen_chats.get(chat_id, False)
    riesgo = (analysis or {}).get("nivel_riesgo", "ninguno")
    alerta = riesgo in ("alto", "emergencia")

    # system prompt (solo dataset + reglas)
    system_txt = build_eva_prompt(
        dataset=DATASET,
        input_type=input_type,
        intro=intro,
        alerta=alerta
    )

    # contexto mínimo (solo datos del analizador + texto)
    contexto = {
        "texto_usuario": user_text,
        "analisis": {
            "sentimiento": (analysis or {}).get("sentimiento"),
            "nivel_riesgo": riesgo,
            "categoria_top": (analysis or {}).get("categoria_top"),
            "score_top": (analysis or {}).get("score_top"),
            "tags": (analysis or {}).get("tags", []),
        }
    }

    messages = [
        {"role": "system", "content": system_txt},
        {"role": "user", "content": json.dumps(contexto, ensure_ascii=False)}
    ]
    reply = ask_llm(messages, temperature=0.15, max_tokens=180)

    # marca saludo usado
    _seen_chats[chat_id] = True
    return reply

# ---------------------- CALLBACKS ----------------------
def _reply_if_any(message: tlb.types.Message, text: str, input_type: str):
    analysis = sa.analyze(text)
    out = generate_reply(text, analysis, input_type=input_type, chat_id=message.chat.id)
    if out:
        bot.reply_to(message, out)

def callback_from_voice(message: tlb.types.Message, text: str, analysis: Dict[str, Any]):
    out = generate_reply(text, analysis, input_type="voz", chat_id=message.chat.id)
    if out:
        bot.reply_to(message, out)

def callback_from_image(message: tlb.types.Message, payload: Dict[str, Any]):
    text = (payload or {}).get("ocr_text", "") or ""
    if text.strip():
        _reply_if_any(message, text, input_type="imagen")

@bot.message_handler(content_types=["text"])
def handle_text(message: tlb.types.Message):
    text = message.text or ""
    _reply_if_any(message, text, input_type="texto")

# ---------------------- REGISTRO ----------------------
def register_handlers():
    VoiceAnalyzer(bot=bot, groq_client=groq, sentiment_analyzer=sa).register_handlers(callback_from_voice)
    ImageAnalyzer(bot=bot, groq_client=groq).register_handlers(callback_from_image)

# ---------------------- ARRANQUE ----------------------
if __name__ == "__main__":
    print(f"Base: {BASE_DIR}")
    print(f"Dataset: {DATASET_PATH} → {'OK' if DATASET else 'VACÍO'}")
    print(f"Modelo: {GROQ_MODEL}")
    register_handlers()
    print("Bot listo. Texto, voz e imagen activos.")
    bot.infinity_polling(skip_pending=True)