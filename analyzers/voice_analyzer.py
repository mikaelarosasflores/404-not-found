import telebot as tlb
#----------------------VOICE ANALYZER-------------------------------
class VoiceAnalyzer:
        def __init__(self, bot, groq_client, sentiment_analyzer):
            self.bot = bot
            self.groq_client = groq_client
            self.sentiment = sentiment_analyzer

        def register_handlers(self):

            @self.bot.message_handler(content_types=['voice'])
            def handle_voice_message(message: tlb.types.Message):
                text = self.transcribe_voice(message)
                if not text:
                    self.bot.reply_to(message, "Lo siento mucho, no pude escucharte bien, ¿Podrías repetirlo? 🌻")
                    return

                # 1) MANDA EL TEXTO A SENTIMENT ANALYZER
                analysis = self.sentiment.analyze_text(text)
                riesgo = analysis["nivel_riesgo"]
                respuesta_sentiment = analysis["respuesta_recomendada"]

                #SI HAY RIESGO:
                if riesgo in ("leve", "moderado", "alto"):
                    self.bot.reply_to(message, respuesta_sentiment)
                    return
                
                #NO HAY RIESGO:
                response = self._groq_response(text)

                if response:
                    self.bot.reply_to(message, response)
                else:    
                    self.bot.reply_to(message, "Tuve un problema procesando tu audio, ¿puedes intentarlo otra vez? ✨")
        
        def transcribe_voice(self, texto):
            try:
                file_info = self.bot.get_file(texto.voice.file_id)
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