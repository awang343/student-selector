import telebot
import state
import os
from dotenv import load_dotenv
import logging
import requests

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

telebot.logger.setLevel(logging.CRITICAL)
bot = telebot.TeleBot(TOKEN)
lecture3 = None

def start_telegram_bot(class_instance):
    global lecture3
    lecture3 = class_instance
    bot.infinity_polling()

@bot.message_handler(commands=['select'])
def handle_select(message):
    if state.selection_in_progress:
        bot.send_message(message.chat.id, "Selection already in progress.")
        return
    state.selection_in_progress = True
    selected_student = lecture3.choose_random()
    state.selected_student = selected_student
    
    bot.send_message(message.chat.id, f"Selected student: {selected_student}")
    try:
        requests.post("http://127.0.0.1:5000/animate_selection", json={"selected_student": selected_student})
    except Exception as e:
        print("Error notifying Flask app:", e)
    finally:
        state.selection_in_progress = False


@bot.message_handler(commands=['volunteer'])
def handle_volunteer(message):
    try:
        student_name = message.text[len('/volunteer '):].strip()
        if not student_name:
            bot.send_message(message.chat.id, "Please provide a student name with the command, e.g., /volunteer Alice")
            return

        lecture3.volunteer(name=student_name)
        bot.send_message(message.chat.id, f"Volunteered: {student_name}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

def send_message(text):
    bot.send_message(CHAT_ID, text)
