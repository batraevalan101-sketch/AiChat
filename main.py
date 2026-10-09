import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

genai.configure(api_key=os.environ["GEMINI_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

chats = {}

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id not in chats:
        chats[user_id] = model.start_chat()
    
    response = chats[user_id].send_message(text)
    await update.message.reply_text(response.text)

app = ApplicationBuilder().token(os.environ["TG_TOKEN"]).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()
