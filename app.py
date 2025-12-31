import os
import threading
from flask import Flask, render_template
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =====================
# CONFIG
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Render ENV variable
PORT = int(os.getenv("PORT", 10000))

# =====================
# FLASK APP (WEBSITE)
# =====================
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status")
def status():
    return {"status": "Bot & Website Running ✅"}

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

# =====================
# TELEGRAM BOT
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot is LIVE!\n🌐 Website connected successfully."
    )

def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

# =====================
# MAIN RUN
# =====================
if __name__ == "__main__":
    # Flask ko alag thread me run karo
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Telegram bot run karo
    run_bot()
