from dotenv import load_dotenv
import os, base64
from groq import Groq

load_dotenv("bot/.env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# pixel JPG mínimo (base64 de 1x1 blanco)
tiny_b64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAIBAQEBAQEBAQEBAQEB..."  # cualquier jpg pequeño válido
# si querés: usa una imagen real que tengas -> b64 = base64.b64encode(open("test.jpg","rb").read()).decode()

resp = client.chat.completions.create(
    model="llama-3.2-11b-vision-preview",
    temperature=0.2,
    max_tokens=20,
    messages=[{
        "role": "user",
        "content": [
            {"type":"text","text":"¿Qué ves? responde 'ok visión' si ves algo."},
            {"type":"input_image","image_url":{"url": f"data:image/jpeg;base64,{tiny_b64}"}}
        ]
    }],
)
print(resp.choices[0].message.content)