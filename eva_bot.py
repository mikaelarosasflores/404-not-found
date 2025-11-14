import os
import telebot as tlb
from groq import Groq
from dotenv import load_dotenv

from analyzers.sentiment_analyzer import SentimentAnalyzer
from analyzers.voice_analyzer import VoiceAnalyzer


#MAIN