import telebot as tlb
import os 
import json
from groq import Groq
from typing import Optional
import time
from dotenv import load_dotenv

#----------------------TEST DE DATOS--------------------------------
#-------------------------------------
# ==========================
#   CONFIGURACIÓN DEL BOT
# ==========================

# Cargar variables del archivo .env
load_dotenv()

TELEGRAM_TOKEN = ""
GROQ_API_KEY = ""

if not TELEGRAM_TOKEN:
    raise ValueError("❌ Falta TELEGRAM_TOKEN en .env")

if not GROQ_API_KEY:
    raise ValueError("❌ Falta GROQ_API_KEY en .env")

# Crear instancias principales
bot = tlb.TeleBot(TELEGRAM_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

# Dataset mínimo para que la clase no falle
dataset = {
    "company_info": {"name": "Bot de Prueba"}
}

# System prompt simple para testear
system_prompt = "Eres un asistente de prueba, responde de forma breve."

# IMPORTANTE:
# VoiceAnalyzer debe estar definida más abajo
# o en otro archivo con import



#-----------------------------------------
def get_groq_response(texto):
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print("Error Groq:", e)
        return None
    
#----------------------TEST DE DATOS--------------------------------



#----------------------VOICE ANALYZER-------------------------------
class VoiceAnalyzer:
        def __init__(self, bot, groq_client, dataset, system_prompt):
            self.bot = bot
            self.groq_client = groq_client
            self.dataset = dataset
            self.system_prompt = system_prompt


        def register_handlers(self):

            @self.bot.message_handler(content_types=['voice'])
            def handle_voice_message(message: tlb.types.Message):
                transcription = self.transcribe_voice(message)
                if not transcription:
                    self.bot.reply_to(message, "Lo siento mucho, no pude escucharte bien, ¿Podrías repetirlo? 🌻")
                    return

                response = get_groq_response(transcription)
                if response:
                    self.bot.reply_to(message,  response)
                else: 
                    self.bot.reply_to(message,"No pude procesar tu mensaje, inténtalo de nuevo en unos segundos. ✨")
        
        def transcribe_voice(self, message):
            try:
                file_info = self.bot.get_file(message.voice.file_id)
                download_file = self.bot.download_file(file_info.file_path)
                
                #archivo temporal:
                temp_file = "temp_voice.ogg"
                with open(temp_file, "wb") as f:
                    f.write(download_file)

                with open(temp_file, "rb") as file:
                    transcription = self.groq_client.audio.transcriptions.create(
                    file=(temp_file, file.read()),
                    model="whisper-large-v3-turbo",
                    prompt="Especificar contexto o pronunciacion",
                    response_format="json",
                    language="es",
                    temperature=1
                )

                # eliminar archivo temporal
                os.remove(temp_file)

        # devolver texto
                return transcription.text

            except Exception as e:
                    print(f"Error al transcribir: {str(e)}")
                    return None
            

#prueba
if __name__ == "__main__":
    voice = VoiceAnalyzer(bot, groq_client, dataset, system_prompt)
    voice.register_handlers()

    print("🎙️ Bot de VOZ en modo prueba listo. Envíame un audio.")
    bot.polling()