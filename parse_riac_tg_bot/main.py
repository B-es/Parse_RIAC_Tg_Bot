import asyncio
import time
import threading 
from termcolor import cprint
from News import News
from Database import Database
from parsing.parser_1 import parsing_site, search_last_news_12page_number
from config import config
from tg_bot.bot import start_bot
from tomita import tomita
from datetime import datetime

database: Database = Database()

def timer():
    """Управляем функция для счёта прошедшего времени паралелльно выполнению другой функции"""
    
    t = threading.current_thread()
    seconds = 1
    while getattr(t, "do_run", True):
        mins, secs = divmod(seconds, 60)
        cprint("Прошло: {:02d}:{:02d}".format(mins, secs), color='red', attrs=["bold"])
        time.sleep(1)
        seconds += 1
    cprint("Прошло всего: {:02d}:{:02d}".format(mins, secs), color='red', attrs=['bold', 'underline'])

async def dataCollection():
    """Собирает данные с 10008 страниц и сохраняет в базу данных"""
    
    if database.getNewsCount() == 834*12: return #10008

    t = threading.Thread(target=timer) #Запуск таймера
    t.start()
    start_time = time.time() #Засекаем время выполнения
    
    captions, links, dates, texts = await parsing_site() #Все значения заданных полей
    news_list: list[tuple] = [(captions[i], links[i], dates[i], texts[i]) for i in range(len(captions))] #Кортежи для сохранения в базу данных
    database.addList(news_list) #Сохранение в базу данных
    
    seconds = time.time() - start_time #Вывод результат
    minutes = seconds / 60
    cprint("--- Сбор закончена ---", color="green")
    cprint("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes), color="green") 
    t.do_run = False #Остановка таймера
    
async def dataUpdating():
    """Добавляет новые данные и сохраняет в базу данных"""
    
    t = threading.Thread(target=timer) #Запуск таймера
    t.start()
    start_time = time.time() #Засекаем время выполнения
    
    lastDate_str = database.getLast()[3]
    lastDate = datetime.strptime(lastDate_str, '%Y-%m-%d %H:%M:%S')
    
    number = await search_last_news_12page_number(lastDate)
    captions, links, dates, texts = await parsing_site(start_page=number) #Все значения заданных полей
    
    index = dates.index(lastDate) + 1
    captions = captions[index:]
    links = links[index:]
    dates = dates[index:]
    texts = texts[index:]
    time.sleep(10)
    news_list: list[tuple] = [(captions[i], links[i], dates[i], texts[i]) for i in range(len(captions))] #Кортежи для сохранения в базу данных
    database.addList(news_list) #Сохранение в базу данных
    
    seconds = time.time() - start_time #Вывод результат
    minutes = seconds / 60
    cprint("--- Актуализация закончена ---", color="green")
    cprint(f"--- Добавлено: {len(captions)} новостей ---", color="green")
    cprint("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes), color="green") 
    t.do_run = False #Остановка таймера
    
def dataFromDatabase() -> list[News]:
    """Выводит все значения из базы данных в виде списка из объектов дата-класса"""
    
    news_list: list[tuple] = [News(*data) for data in database.getList()]
    return news_list
    
def newsAddition(news_list: list[News]):
    sql = '''UPDATE News SET vips = ?, attractions = ? WHERE id = ?'''
    database.openConnection()
    for news in news_list:
        vips = []
        attractions = []
        if news.vips != None: vips = news.vips
        if news.attractions != None: attractions = news.attractions
        print((','.join(vips), ','.join(attractions)))
        print(news.number)
        database.executeSql(sql, (','.join(vips), ','.join(attractions), news.number))
    database.closeConnection

if __name__ == "__main__":
    asyncio.run(dataUpdating())
    # news_list = dataFromDatabase()[3:10]
    # tomita.vips_attractions_collection(news_list)
    # print([(news.vips, news.attractions) for news in news_list])
    #start_bot()
    
    
    
    
    
    