import asyncio
import time
import threading 
import colorama
from parsing.News import News
from database import Database
from parsing.parser_1 import parsing_site
from config import config

def timer():
    t = threading.current_thread()
    el = 1
    while getattr(t, "do_run", True):
        print(colorama.Fore.RED + f"Прошло: {el} секунд | {el/60:.4f} минут")
        time.sleep(1)
        el += 1
    print(colorama.Fore.RED + f"Прошло всего: {el} секунд | {el/60:.4f} минут")

async def dataCollection():
    database: Database = Database()
    
    if database.getNewsCount() == 834*12: return #10008
    
    site = config.get("site") #Основная ссылка
    headers = config.get("headers") #Заголовки для отправки
    news_page = config.get("news_page")
    start_page = config.get("start_page")
    last_page = config.get("last_page")

    t = threading.Thread(target=timer)
    t.start()
    start_time = time.time()
    captions, links, dates, texts = await parsing_site(site, news_page, headers, start_page=start_page, last_page=last_page)
    news_list: list[News] = [News(i+1,captions[i], links[i], dates[i], texts[i]) for i in range(len(captions))]
    database.addList(news_list)
    seconds = time.time() - start_time
    minutes = seconds / 60
    print("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes))
    t.do_run = False

if __name__ == "__main__":
    colorama.init(autoreset=False)
    asyncio.run(dataCollection())
    