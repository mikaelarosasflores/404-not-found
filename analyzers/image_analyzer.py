# ====================== file: analyzers/image_analyzer.py ======================
import telebot as tlb
import io, json, base64
from typing import Any, Dict, Callable, Optional
from PIL import Image

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

class ImageAnalyzer:
    def __init__(self, bot: tlb.TeleBot, groq_client: Any, model: str = VISION_MODEL):
        self.bot = bot
        self.groq = groq_client
        self.model = model

    def register_handlers(self, callback_main: Callable[[tlb.types.Message, Dict[str, Any]], None]):
        @self.bot.message_handler(content_types=["photo"])
        def handle_photo(message: tlb.types.Message):
            payload = self._analyze_message_image(message, self._download_photo_bytes(message))
            callback_main(message, payload)

        @self.bot.message_handler(content_types=["document"])
        def handle_document(message: tlb.types.Message):
            doc = message.document
            if not doc or not (doc.mime_type or "").startswith("image/"):
                return
            payload = self._analyze_message_image(message, self._download_doc_bytes(message))
            callback_main(message, payload)

    # ---- helpers ----
    def _download_photo_bytes(self, message: tlb.types.Message) -> Optional[bytes]:
        try:
            ph = message.photo[-1]
            fi = self.bot.get_file(ph.file_id)
            return self.bot.download_file(fi.file_path)
        except Exception:
            return None

    def _download_doc_bytes(self, message: tlb.types.Message) -> Optional[bytes]:
        try:
            fi = self.bot.get_file(message.document.file_id)
            return self.bot.download_file(fi.file_path)
        except Exception:
            return None

    def _to_jpeg_b64(self, data: bytes, max_side: int = 2000) -> Optional[str]:
        try:
            img = Image.open(io.BytesIO(data)).convert("RGB")
            w, h = img.size
            s = max(w, h) / max_side
            if s > 1:
                img = img.resize((int(w / s), int(h / s)), Image.LANCZOS)
            out = io.BytesIO()
            img.save(out, format="JPEG", quality=92)
            return base64.b64encode(out.getvalue()).decode("utf-8")
        except Exception:
            return None

    # ---- visión ----
    def _call_vision(self, b64_jpeg: str) -> Dict[str, Any]:
        try:
            prompt = (
                "Extrae texto en ESPAÑOL de una captura de pantalla (chat/WhatsApp). "
                "Devuelve SOLO JSON con claves:\n"
                "ocr_text: string (todo el texto visible, líneas separadas por \\n),\n"
                "objects: lista máx 5 de {label, prob}.\n"
                "Si no hay texto, usa ocr_text=\"\"."
            )
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_jpeg}"}},
                ],
            }]
            try:
                resp = self.groq.chat.completions.create(
                    model=self.model,
                    temperature=0.0,
                    response_format={"type": "json_object"},
                    messages=messages,
                )
                text = resp.choices[0].message.content
            except Exception:
                resp = self.groq.chat.completions.create(
                    model=self.model,
                    temperature=0.0,
                    messages=messages,
                )
                text = resp.choices[0].message.content
            return json.loads(text)
        except Exception as e:
            return {"error": str(e)}

    # ---- core ----
    def _analyze_message_image(self, message: tlb.types.Message, img_bytes: Optional[bytes]) -> Dict[str, Any]:
        meta = {
            "user_id": getattr(message.from_user, "id", None),
            "chat_id": getattr(message.chat, "id", None),
            "message_id": getattr(message, "message_id", None),
        }
        if not img_bytes:
            return {"status": "error", "reason": "download_failed", "meta": meta}
        b64 = self._to_jpeg_b64(img_bytes)
        if not b64:
            return {"status": "error", "reason": "encode_failed", "meta": meta}

        out = self._call_vision(b64)
        if "error" in out:
            return {"status": "error", "reason": "vision_error", "error": out["error"], "meta": meta}

        ocr = (out.get("ocr_text") or "").strip()
        return {
            "status": "ok",
            "meta": meta,
            "ocr_text": ocr,
            "objects": out.get("objects", []) or [],
        }
