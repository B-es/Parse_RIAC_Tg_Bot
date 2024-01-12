import asyncio
import time
import threading 
from termcolor import cprint
from parsing.News import News
from Database import Database
from parsing.parser_1 import parsing_site
from config import config
from tg_bot.bot import start_bot
from tomita import tomita

database: Database = Database()

def timer():
    """Управляем функция для счёта прошедшего времени паралелльно выполнению другой функции"""
    
    t = threading.current_thread()
    el = 1
    while getattr(t, "do_run", True):
        cprint(f"Прошло: {el} секунд | {el/60:.4f} минут", color='red', attrs=["bold"])
        time.sleep(1)
        el += 1
    cprint(f"Прошло всего: {el} секунд | {el/60:.4f} минут", color='red', attrs=['bold', 'underline'])

async def dataCollection():
    """Собирает данные с 10008 страниц и сохраняет в базу данных"""
    
    if database.getNewsCount() == 834*12: return #10008
    
    site = config.get("site") #Основная ссылка
    headers = config.get("headers") #Заголовки для отправки
    news_page = config.get("news_page") #Шаблон ссылки на страницу
    start_page = config.get("start_page") #Первая страница
    last_page = config.get("last_page") #Последняя страница

    t = threading.Thread(target=timer) #Запуск таймера
    t.start()
    start_time = time.time() #Засекаем время выполнения
    
    captions, links, dates, texts = await parsing_site(site, news_page, headers, start_page=start_page, last_page=last_page) #Все значения заданных полей
    news_list: list[tuple] = [(captions[i], links[i], dates[i], texts[i]) for i in range(len(captions))] #Кортежи для сохранения в базу данных
    database.addList(news_list) #Сохранение в базу данных
    
    seconds = time.time() - start_time #Вывод результат
    minutes = seconds / 60
    cprint("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes), color="green") 
    t.do_run = False #Остановка таймера
    
def dataFromDatabase() -> list[News]:
    """Выводит все значения из базы данных в виде списка из объектов дата-класса"""
    
    news_list: list[tuple] = [News(*data) for data in database.getList()]
    return news_list
    

if __name__ == "__main__":
    # asyncio.run(dataCollection())
    # news_list = dataFromDatabase()
    # print(news_list[-1])
    start_bot()