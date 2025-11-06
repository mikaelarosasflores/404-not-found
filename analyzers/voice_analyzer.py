import telebot as tlb
import os
import json
import time
from typing import Optional
from groq import Groq
from dotenv import load_dotenv

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.system_prompt import build_eva_prompt


class VoiceAnalyzer:  #Esta es la clase que engloba todo el comportamiento del analizador de voz del bot EVA, con la idea de que sea reutilizable

    def __init__(self,  dataset_path: str = "../data/dataset.json"):

        #Carga las variables de .env
        load_dotenv()

        #Obtener tokens
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")
        self.groq_api_key = os.getenv("GROQ_API_KEY")

        #Validación...
        if not self.telegram_token:
                raise ValueError("❌ Falta TELEGRAM_TOKEN en .env")
        if not self.groq_api_key:
                raise ValueError("❌ Falta GROQ_API_KEY en .env")

        #Instanciar objetos principales
        self.bot = tlb.TeleBot(self.telegram_token)
        self.groq_client = Groq(api_key=self.groq_api_key)

        #Llamar dataset
        self.company_info = self._load_dataset(dataset_path)

        #Llamar handlers
        self._register_handlers()


    #Cargar el dataset
    def _load_dataset(self, path: str):
        try:
            # 🧭 Obtener ruta absoluta del archivo
            base_dir = os.path.dirname(os.path.abspath(__file__))  # /analyzers
            abs_path = os.path.join(base_dir, "..", "data", "dataset.json")
            abs_path = os.path.normpath(abs_path)  # Limpia la ruta final
            print(f"📂 Buscando dataset en: {abs_path}")

            # 📖 Intentar leer el archivo
            with open(abs_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"✅ Dataset cargado correctamente: {data['company_info']['name']}")
            return data

        except FileNotFoundError:
            print(f"⚠️ No se encontró el dataset en {abs_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error en formato JSON del dataset: {e}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado al cargar dataset: {e}")
        return None

        
    #Registrar handlers
    def _register_handlers(self):
        @self.bot.message_handler(content_types=['voice'])
        def voice_handler(message):
            self._handle_voice_message(message)
        print("📡 Handler de voz registrado correctamente.")

        
        @self.bot.message_handler(commands=['start', 'hola'])
        def start_handler(message):
            self.bot.reply_to(message, "👋 ¡Hola! EVA está activa y lista para escucharte.")

        @self.bot.message_handler(content_types=['text'])
        def text_handler(message):
            try:
                user_message = message.text.strip()
                print(f"💬 Mensaje de texto recibido: {user_message}")

                # Mostrar acción "escribiendo"
                self.bot.send_chat_action(message.chat.id, "typing")

                # Obtener respuesta de Groq
                response = self._get_groq_response(user_message)

                if response:
                    self.bot.reply_to(message, response)
                    print(f"✅ Respuesta enviada: {response[:80]}...")
                else:
                    self.bot.reply_to(message, "No tengo una respuesta para eso 😅, pero puedo escucharte si quieres hablar.")
            except Exception as e:
                print(f"❌ Error en text_handler: {e}")
                self.bot.reply_to(message, "Hubo un error procesando tu mensaje 😔.")




    def _get_groq_response(self, user_message: str) -> Optional[str]:
        try:
            system_prompt = build_eva_prompt(self.company_info, input_type="voz")
            completion = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.2,           # más bajo = más fiel al dataset
                max_tokens=500,            # límite razonable de salida
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message.strip()}
                ]
            )
            content = completion.choices[0].message.content.strip()
            return content if content else None

        except Exception as e:
            print(f"❌ Error en _get_groq_response: {str(e)}")
            return None

    def _transcribe_voice(self, message: tlb.types.Message) -> Optional[str]:
        try:
            file_info = self.bot.get_file(message.voice.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            temp_file = "temp_voice.ogg"
            with open(temp_file, "wb") as f:
                 f.write(downloaded_file)
            with open(temp_file, "rb") as audio_file:
                 transcription = self.groq_client.audio.transcriptions.create(
                    file=(temp_file, audio_file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    language="es",
                    temperature=0.2
                 )
            os.remove(temp_file)
            text = transcription.text.strip()
            print(f"🗣️ Transcripción completada: {text[:60]}...")  # preview
            return text

        except Exception as e:
            print(f"❌ Error en _transcribe_voice: {str(e)}")
            return None
        
    def _handle_voice_message(self, message: tlb.types.Message):
        try:
            self.bot.send_chat_action(message.chat.id, "typing")
            print("🎧 Recibido mensaje de voz, procesando...")
            text = self._transcribe_voice(message)
            
            if not text:
                self.bot.reply_to(message, "No pude entender el audio 😔, ¿podrías repetirlo?")
                return
            print(f"📝 Texto detectado: {text}")
            response = self._get_groq_response(text)

            if not response: 
                self.bot.reply_to(message, "Tuve un problema procesando el mensaje 😕, inténtalo otra vez.")
                return
            
            self.bot.reply_to(message, response)
            print(f"💬 Respuesta enviada: {response[:80]}...")

        except Exception as e:
            print(f"❌ Error en _handle_voice_message: {str(e)}")
            self.bot.reply_to(message, "Hubo un error al procesar tu audio 😔.")

if __name__ == "__main__":
    print("🧠 Iniciando bot de voz EVA...")
    try:
        eva = VoiceAnalyzer()
        print("✅ Bot inicializado correctamente.")
        # 🔁 Bucle de reconexión automática
        while True:
            try:
                print("🚀 EVA escuchando mensajes...")
                eva.bot.polling(non_stop=True, timeout=60, long_polling_timeout=5)
            except Exception as poll_error:
                print(f"⚠️ Error interno en polling: {type(poll_error).__name__} -> {poll_error}")
                time.sleep(3)
                print("🔁 Reintentando conexión...\n")

    except Exception as e:
        print(f"❌ Error crítico al iniciar EVA: {e}")