import os
from dotenv import load_dotenv
import telebot
from groq import Groq
from analyzers.sentiment_analyzer import analyze_sentiment

# Cargar variables de entorno
load_dotenv()

# Configurar tokens - PEGA TU TOKEN AQUI
TELEGRAM_TOKEN = "8464037430:AAENCAkvEvM2MPbrHIuRUu9HrfcQOH99EZE"
GROQ_API_KEY = os.getenv("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")

# Inicializar bot y Groq
bot = telebot.TeleBot(8464037430:AAENCAkvEvM2MPbrHIuRUu9HrfcQOH99EZE)
groq_client = Groq(api_key=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)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text
    print(f"📨 Mensaje recibido: {user_text}")
    
    # 1. PRIMERO usar TU analyzer de sentimientos
    sentiment_result = analyze_sentiment(user_text)
    print(f"🔍 Análisis: {sentiment_result}")
    
    # 2. Si hay riesgo, responder con TU sistema
    if sentiment_result['risk_level'] in ['high', 'medium']:
        response = f"⚠️ {sentiment_result['response']}"
        print(f"🚨 Respuesta de riesgo: {response}")
        bot.reply_to(message, response)
        return
    
    # 3. Si es seguro, usar Groq para respuesta normal
    try:
        print("🤖 Consultando Groq...")
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": user_text}],
            model="llama3-8b-8192",
        )
        groq_response = chat_completion.choices[0].message.content
        print(f"💬 Respuesta Groq: {groq_response}")
        bot.reply_to(message, groq_response)
        
    except Exception as e:
        print(f"❌ Error con Groq: {e}")
        bot.reply_to(message, "🤖 Hola! Soy EvaBot. ¿En qué puedo ayudarte?")

if __name__ == "__main__":
    print("🤖 EvaBot con Análisis de Sentimientos iniciado...")
    print("📱 Bot listo para recibir mensajes...")
    bot.polling()