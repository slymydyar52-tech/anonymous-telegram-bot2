import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("BOT_TOKEN")      # از Railway
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "👑 ادمین عزیز، ربات ناشناس فعال است!")
    else:
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton("📩 ارسال پیام ناشناس", callback_data="anon")
        markup.add(btn)
        bot.reply_to(message, "🔒 برای ارسال پیام ناشناس دکمه زیر را بزن!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "anon")
def anon_start(call):
    bot.edit_message_text("✍️ پیام ناشناس خود را بنویس:", call.message.chat.id, call.message.message_id)


@bot.message_handler(func=lambda message: True)
def handle_message(message):

    # ادمین در حال جواب دادن
    if message.from_user.id == ADMIN_ID and message.reply_to_message:
        if "[ID:" in message.reply_to_message.text:
            try:
                user_id = int(message.reply_to_message.text.split("[ID:")[1].split("]")[0])
                bot.send_message(user_id, f"💬 جواب ادمین:\n\n{message.text}")
                bot.reply_to(message, "✅ ارسال شد!")
                return
            except:
                bot.reply_to(message, "❌ خطا در ارسال!")
                return

    # کاربر ناشناس پیام می‌دهد
    if message.from_user.id != ADMIN_ID:
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton("💬 جواب", callback_data=f"reply_{message.from_user.id}")
        markup.add(btn)

        text = (
            f"👤 پیام ناشناس جدید:\n\n"
            f"{message.text}\n\n"
            f"ID: [ID: {message.from_user.id}]"
        )

        bot.send_message(ADMIN_ID, text, reply_markup=markup)
        bot.reply_to(message, "✅ پیامت رسید! منتظر جواب باش.")


print("🚀 ربات ناشناس 24/7 آماده شد!")
bot.infinity_polling()
