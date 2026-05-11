import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from threading import Thread
from flask import Flask

# === RENDER KE LIYE DUMMY SERVER ===
app = Flask('')
@app.route('/')
def home():
    return "Bhai AI Zinda Hai 🔥"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
# ===================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Haan bhai, main zinda hu 🔥 Bol kya kaam hai?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(f"Tu ek 'Bhai' hai. Dosti wale, funny, aur thode savage andaaz mein is sawaal ka jawaab de: {user_message}")
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Bhai abhi dimaag hang ho gaya, 2 min baad try kariyo 😅")

if __name__ == '__main__':
    print("Bhai AI Zinda Hai 🔥")
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
