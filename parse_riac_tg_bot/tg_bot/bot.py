from env import apikey
from telebot import TeleBot

bot = TeleBot(apikey)

#TODO: Добавить весь функционал в бота
#!: 1) Вывод в форматированном тексте
#!: 2) Операция после ввода слова человека

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Помощи не будет")
        
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Помощи не будет")
    
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Здраво":
        bot.send_message(message.from_user.id, "Я живой")
    elif message.text != 'help':
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

def start_bot():
    bot.polling(none_stop=True, interval=0)
    
        