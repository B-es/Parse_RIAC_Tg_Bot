from datetime import datetime
from parsing.News import News
from database import Database
from parsing.parser_1 import parsing_site
from config import config

def dataCollection():
    database: Database = Database()
    
    if database.getNewsCount() == 834*12: return #10008
    
    site = config.get("site") #Основная ссылка
    headers = config.get("headers") #Заголовки для отправки

    captions: list[str] = [] #Заголовки
    links: list[str] = [] #Ссылки
    dates: list[datetime] = [] #Даты
    texts: list[str] = [] #Текст новостей

    import time
    start_time = time.time()
    i = 835
    while i > 0:
        start_time_in = time.time()
        news_page = site + f'/news/?PAGEN_1={i}' #Страница с новостями под номером i
        i -= 1
        res = parsing_site(site, news_page, headers)
        captions = res[0]
        links = res[1]
        dates = res[2]
        texts = res[3]
        news_list: list[News] = [News(captions[i], links[i], dates[i], texts[i]) for i in range(len(captions))]
        database.addList(news_list)
        seconds = time.time() - start_time_in
        minutes = seconds / 60
        print(f"Страница {i}: проанализирована\nВремя выполнения:\n{seconds:.4f} секунд\n{minutes:.4f} минут")
    seconds = time.time() - start_time
    minutes = seconds / 60
    print("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes))

    
    #news = News(captions[0], links[0], dates[0], texts[0])
    

    


if __name__ == "__main__":
    dataCollection()