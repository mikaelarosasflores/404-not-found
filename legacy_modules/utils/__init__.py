import base64, re
from io import BytesIO
from PIL import Image

def clean_key(k: str) -> str:
    if not k:
        return ""
    for ch in ["\ufeff", "\u200b", "\u200c", "\u200d", "\u2060", "\uFEFF"]:
        k = k.replace(ch, "")
    return re.sub(r"[^A-Za-z0-9_\-]", "", k.strip())

def downscale_if_needed(image_bytes: bytes, max_side: int = 1600, jpeg_quality: int = 85) -> bytes:
    try:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        w, h = img.size
        scale = max(w, h) / max_side
        if scale > 1:
            img = img.resize((int(w/scale), int(h/scale)), Image.LANCZOS)
        out = BytesIO()
        img.save(out, format="JPEG", quality=jpeg_quality, optimize=True)
        return out.getvalue()
    except Exception:
        return image_bytes

def bytes_to_b64(b: bytes) -> str:
    return base64.b64encode(b).decode("utf-8")