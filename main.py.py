import telebot
import re
from flask import Flask
from threading import Thread

# === CONFIG ===
TOKEN = '7701217661:AAE61OMv_c0H50T1rBnQ4xZsbeS8sxJvWf0'  # Bot tokeningiz
ADMIN_IDS = [6548564636, 7139344893, 7189291937, 6880867791]  # Admin Telegram ID'lar

bot = telebot.TeleBot(TOKEN)
correct_answers = []

# === Flask server for uptime bot ===
app = Flask('')

@app.route('/')
def home():
    return "Men tirikman!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# === Telegram Bot Handlers ===

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(
        message.chat.id,
        "👋 Javoblaringizni quyidagicha yuboring: 1a2c3b4d...\n"
        "Adminlar to‘g‘ri javoblarni quyidagicha o‘rnata oladi: /setanswers 1a2c3b4d",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['setanswers'])
def set_answers(message):
    global correct_answers
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "❌ Siz javoblarni o‘rnatishga ruxsat etilmagansiz.")
        return

    text = message.text.replace("/setanswers", "").upper().replace(" ", "")
    extracted = re.findall(r'\d+([A-D])', text)

    if not extracted:
        bot.send_message(message.chat.id, "⚠️ Format quyidagicha bo'lishi kerak: /setanswers 1a2c3d4b")
        return

    correct_answers = extracted
    bot.send_message(message.chat.id, f"✅ To‘g‘ri javoblar saqlandi! Umumiy: {len(correct_answers)} ta")

@bot.message_handler(func=lambda message: True)
def check_user_answers(message):
    if not correct_answers:
        bot.send_message(message.chat.id, "⚠️ Hali to‘g‘ri javoblar o‘rnatilmagan.")
        return

    text = message.text.upper().replace(" ", "")
    user_answers = re.findall(r'\d+([A-D])', text)

    if len(user_answers) != len(correct_answers):
        bot.send_message(
            message.chat.id,
            f"⚠️ Siz {len(correct_answers)} ta javob yuborishingiz kerak.\nSiz yuborgansiz: {len(user_answers)} ta."
        )
        return

    result_lines = []
    correct = 0

    for i, (user_ans, correct_ans) in enumerate(zip(user_answers, correct_answers), start=1):
        if user_ans == correct_ans:
            result_lines.append(f"{i} ✅")
            correct += 1
        else:
            result_lines.append(f"{i} ❌")

    wrong = len(correct_answers) - correct
    result_lines.append(f"\n✅ To‘g‘ri: {correct}")
    result_lines.append(f"❌ Noto‘g‘ri: {wrong}")

    bot.send_message(message.chat.id, "\n".join(result_lines))

# === Run bot + uptime server ===
keep_alive()
bot.polling()
