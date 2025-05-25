import telebot
from telebot import types

API_TOKEN = '7987776972:AAFcUZ3Tf4GBeLl4mONaQiHV2MqDr3qz8r8'
ADMIN_ID = 465513095

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    buy_button = types.InlineKeyboardButton("💸 Купить абуз «Мегамаркет» – 300₽", url="https://www.donationalerts.com/r/danil222711")
    markup.add(buy_button)
    bot.reply_to(message, "Привет! Готов получить жирный абуз?👇", reply_markup=markup)
    bot.send_message(message.chat.id, "После оплаты пришли скриншот сюда.")

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    bot.send_message(ADMIN_ID, f"📸 Скрин от @{message.from_user.username or message.from_user.id}")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

@bot.message_handler(commands=['выдать'])
def send_file(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Укажи пользователя: /выдать @username")
            return
        username = parts[1].lstrip('@')
        user = bot.get_chat(username)
        doc = open('abuz_megamarket.pdf', 'rb')
        bot.send_document(user.id, doc, caption="📄 Вот твой абуз. Удачного заработка!")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

bot.polling()
