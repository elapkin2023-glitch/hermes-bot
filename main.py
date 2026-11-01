from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from groq import Groq
import os
from flask import Flask
import threading

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
client = Groq(api_key=GROQ_KEY)

# Web server biar Render Free gak tidur
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Hermes Bot Hidup!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

async def jawab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pesan = update.message.text
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Kamu Hermes Agent AI, jawab pakai bahasa Indonesia santai."},
                {"role": "user", "content": pesan}
            ]
        )
        await update.message.reply_text(chat.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, jawab))
    print("Hermes Online!")
    app.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_bot()
