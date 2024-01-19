from env import apikey
from telebot.async_telebot import AsyncTeleBot 
from actions import dataFromDatabase, getSynonyms, dataUpdating, isNew
from apscheduler.schedulers.asyncio import AsyncIOScheduler

seconds = 0
scheduler = AsyncIOScheduler()
job = scheduler.add_job(dataUpdating, 'interval', seconds=100)
bot = AsyncTeleBot(apikey)
news_list = dataFromDatabase()

chat_id = ''

async def listener():
    if isNew[0]:
        await bot.send_message(chat_id, dataFromDatabase()[-1].__repr__())
    else:
        print("Нет новых новостей")
            
scheduler.add_job(listener, 'interval', seconds=100)

help = """
Чат-Бот для вывода следующей информации:
- Название новости
- Дата новости
- Ссылка на новость
- Текст новости
- VIP-персоны
- Достопримечательности
Описание команд:
'/news' - вывод последней новости
'/news ❮номер новости❯' - вывод конкретной новости по ID в БД
'/synonyms ❮слово❯ ❮число синонимов❯' - вывод контекстных синонимов на всём объеме новостных статей из БД
'/pause_schedule' - остановка обновления БД новостей
'/resume_schedule' - возобновления обновления БД новостей
'/schedule  ❮интервал обновления БД❯' - запуск обновления БД новостей
"""

@bot.message_handler(commands=['pause_schedule'])
async def send_pause_schedul(message):
    job.pause()
    await bot.reply_to(message, "Задача приостановлена")
    
@bot.message_handler(commands=['resume_schedule'])
async def send_pause_schedul(message):
    job.resume()
    await bot.reply_to(message, "Задача возабновлена")

@bot.message_handler(commands=['schedule'])
async def send_schedul(message):
    splt: list[str] = message.text.split(' ')
    text = "Неверный ввод"
    
    if len(splt) != 2:
        await bot.reply_to(message, text)
        return
    
    if splt[1].isdigit():
        global job
        job.reschedule("interval", seconds=int(splt[1]))
        if scheduler.state == 0:
            scheduler.start()
        await bot.reply_to(message, f"Интервал установлен на {splt[1]}")
        
@bot.message_handler(commands=['start', 'help'])
async def send_help(message):
    global chat_id
    chat_id = message.from_user.id
    await bot.reply_to(message, help)
    
@bot.message_handler(commands=['news'])
async def send_news(message):
    splt: list[str] = message.text.split(' ')
    text = "Неверный ввод"
    
    if len(splt) > 1:
        if splt[1].isdigit():
            number = int(splt[1])
            if len(news_list) > number > 0:
                text = news_list[number-1].__repr__()
    else:
        text = news_list[-1].__repr__()
    
    await bot.reply_to(message, text)
    
@bot.message_handler(commands=['synonyms'])
async def send_synonyms(message):
    
    splt: list[str] = message.text.split(' ')
    text = "Неверный ввод"
    count = 1
    
    if len(splt) > 1:
        if splt[1].isalpha():
            if len(splt) == 3: 
                if splt[2].isdigit():
                    count = int(splt[2])
                else:
                    await bot.reply_to(message, text)
                    return
            await bot.reply_to(message, "Подождите одну минуту")
            res = getSynonyms(splt[1], count)
            if not res: 
                text = "Не нашёл синонимов"
            else:
                text = '\n'.join(res)
        else:
            await bot.reply_to(message, text)
            return
    
    await bot.reply_to(message, text)
    
@bot.message_handler(content_types=['text'])
async def get_text_messages(message):
    if message.text == "Здраво":
        await bot.send_message(message.from_user.id, "Я живой")
    else:
        await bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

async def start_bot():
    await bot.polling(none_stop=True, interval=0)
    
    
        