python-telegram-bot==22.2
openai>=1.0.0
python-dotenv
httpximport os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to GC Trading Coach AI!\n\nSend me your trading question."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert GC Futures Trading Coach. "
                    "Help with risk management, R:R calculation, "
                    "trade psychology and prop firm rules. "
                    "Never guarantee profits."
                ),
            },
            {"role": "user", "content": user_message},
        ],
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()
