from threading import current_thread, Thread
from time import time, sleep
from termcolor import cprint
from News import News
from Database import Database
from parsing.parser_1 import parsing_site, search_last_news_12page_number
from processing.proccessing import processingNews
from tomita import tomita
from datetime import datetime
from spark.searchSynonyms import getContextSynonyms

database: Database = Database()

isNew: list = [False]

def timer():
    """Управляем функция для счёта прошедшего времени паралелльно выполнению другой функции"""
    
    t = current_thread()
    seconds = 1
    while getattr(t, "do_run", True):
        mins, secs = divmod(seconds, 60)
        cprint("Прошло: {:02d}:{:02d}".format(mins, secs), color='red', attrs=["bold"], end='\r')
        sleep(1)
        seconds += 1
    cprint("Прошло всего: {:02d}:{:02d}".format(mins, secs), color='red', attrs=['bold', 'underline'], end='\r')

async def dataCollection():
    """Собирает данные с 10008 страниц и сохраняет в базу данных"""
    
    if database.getNewsCount() == 834*12: return #10008

    t = Thread(target=timer) #Запуск таймера
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
    
    start_time = time() #Засекаем время выполнения
    
    lastDate_str = database.getLast()[3]
    lastDate = datetime.strptime(lastDate_str, '%Y-%m-%d %H:%M:%S')
    
    number = await search_last_news_12page_number(lastDate)
    captions, links, dates, texts = await parsing_site(start_page=number) #Все значения заданных полей
    
    index = dates.index(lastDate) + 1
    captions = captions[index:]
    links = links[index:]
    dates = dates[index:]
    texts = texts[index:]
   
    news_list: list[tuple] = [(captions[i], links[i], dates[i], texts[i]) for i in range(len(captions))] #Кортежи для сохранения в базу данных
    database.addList(news_list) #Сохранение в базу данных
    
    seconds = time() - start_time #Вывод результат
    minutes = seconds / 60
    cprint("--- Актуализация закончена ---", color="green")
    cprint(f"--- Добавлено: {len(captions)} новостей ---", color="green")
    cprint("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes), color="green") 
    
    global isNew
    isNew[0] = False if not captions else True
    
def dataFromDatabase() -> list[News]:
    """Выводит все значения из базы данных в виде списка из объектов дата-класса"""
    
    news_list: list[tuple] = [News(data[0], data[1], data[2], data[3], data[4], data[5].split(' '), data[6].split(' '), data[7], data[8], data[9]) for data in database.getList()]
    return news_list


import keyboard

async def newsAddition(news_list: list[News]):
    
    t = Thread(target=timer) #Запуск таймера
    t.start()
    
    def stop_timer():
        t.do_run = False
    
    keyboard.add_hotkey('f4', stop_timer)
    
    tomita.vips_attractions_collection(news_list)
    database.updateList([news.toUpdate() for news in news_list])
    
    # news_list_with_vips_or_attractions = [news for news in news_list if news.attractions or news.vips]
    # news_without_ton = [news for news in news_list_with_vips_or_attractions if news.annotation == '' or news.annotation == None]
    # texts = [news.text for news in news_without_ton]

    # def split(a, n):
    #     k, m = divmod(len(a), n)
    #     return [a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]

    # sotki = split(texts, 20)
    # sotki_news = split(news_list_with_vips_or_attractions, 20)
    
    # for part, part_news, i in zip(sotki, sotki_news, range(1, 21)):
    #     summarizers, rewriters, tonals = await processingNews(part)
        
    #     for summarizer, rewriter, tonal, news in zip(summarizers, rewriters, tonals, part_news):
    #         news.annotation = summarizer
    #         news.rewrite = rewriter
    #         news.tonality = tonal
        
    #     database.updateList([news.toUpdate() for news in part_news])
    #     cprint(f"{i} сотка загружена", color='red')
    t.do_run = False #Остановка таймера
    
def getSynonyms(word: str, count:int = 1) -> list[str]:
    news_list = dataFromDatabase()
    start_time = time() #Засекаем время выполнения
    res = getContextSynonyms([news.text for news in news_list], word, count)
    
    seconds = time() - start_time #Вывод результат
    minutes = seconds / 60
    cprint("--- Получение контекстных синонимов закончены ---", color="green")
    cprint("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes), color="green") 
    
    return [v for v, freq in res]
    

    