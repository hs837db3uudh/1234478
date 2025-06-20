# main.py

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ✅ आपके टोकन और चैनल ID कोड में ही दिए गए हैं
BOT_TOKEN = "7678597712:AAH1U-s0RvO3CEYNwpW4VZGvn3iELNZSSww"
CHANNEL_ID = "-7025388094"  # Channel ID जहाँ से मूवी खोजनी है

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Hi! मुझे मूवी का नाम भेजो, मैं चैनल से ढूंढकर भेजूंगा।")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    user_id = update.message.from_user.id

    messages = await context.bot.get_chat_history(chat_id=CHANNEL_ID, limit=100)
    found = False
    for msg in messages:
        if msg.caption and query.lower() in msg.caption.lower():
            await context.bot.copy_message(chat_id=user_id, from_chat_id=CHANNEL_ID, message_id=msg.message_id)
            found = True
            break
    if not found:
        await update.message.reply_text("❌ मूवी नहीं मिली। कोई और नाम ट्राय करें।")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()
