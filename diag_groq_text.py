from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv("bot/.env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

resp = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role":"user","content":"Di 'ok texto'"}],
    max_tokens=10,
)
print(resp.choices[0].message.content)