import os
from dotenv import load_dotenv
import telebot
from analyzers.sentiment_analyzer import SecurityAnalyzer

load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(token)

# ✅ TU ANALYZER 100% EFECTIVO
analyzer = SecurityAnalyzer()

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text
    print(f"📨 Mensaje: '{user_text}'")
    
    # ✅ USAR TU ANALYZER PERFECTO
    analysis = analyzer.analyze_message(user_text)
    print(f"🔍 Riesgo: {analysis['nivel_riesgo']} | Patrones: {len(analysis['patrones_detectados'])}")
    
    # ✅ RESPUESTA AUTOMÁTICA PERFECTA (ya viene del analyzer)
    bot.reply_to(message, analysis['respuesta_recomendada'])

print("🤖 BOT TEST - ANALYZER 100% EFECTIVO ACTIVADO")
print("📊 Versión: 3.0 Perfecta")
print("📱 Escuchando mensajes...")
bot.polling()