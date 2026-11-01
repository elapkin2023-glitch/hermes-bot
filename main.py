from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from groq import Groq
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

client = Groq(api_key=GROQ_KEY)

async def jawab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pesan = update.message.text
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Kamu adalah Hermes Agent AI. Jawab pakai bahasa Indonesia, santai, helpful."},
                {"role": "user", "content": pesan}
            ]
        )
        await update.message.reply_text(chat.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, jawab))
print("Hermes Online!")
app.run_polling()
