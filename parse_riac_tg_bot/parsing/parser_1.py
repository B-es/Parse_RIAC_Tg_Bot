import asyncio
import aiohttp
import time
from config import months, config
from bs4 import BeautifulSoup
from datetime import datetime
from termcolor import cprint

site = config.get("site") #Основная ссылка
headers = config.get("headers") #Заголовки для отправки
news_page = config.get("news_page") #Шаблон ссылки на страницу
start_page = config.get("start_page") #Первая страница
last_page = config.get("last_page") #Последняя страница

def parsing_captions_links_dates(page:str, site:str) -> tuple[list, list, list]:
    """
    Парсит 12 заголовков, ссылок и дат с одной страницы
    * page: str - код страницы
    * site - ссылка на сайт
    """
    
    captions: list[str] = [] #Заголовки
    links: list[str] = [] #Ссылки
    dates: list[datetime] = [] #Даты
    soup = BeautifulSoup(page, "html.parser") #Супчик
    allNews = soup.find_all('div', class_="new-block") #Ищем все новости
    #Анализ данных
    for data in allNews:
        captionData = data.find('a', class_='caption')
        if captionData is not None:
            captions.append(captionData.text) #Заголовок
            links.append(site+captionData['href']) #Ссылка
        dateData = data.find('span', class_='date')
        if dateData is not None:
            dates.append(convertData(dateData.text))
    return (captions[::-1], links[::-1], dates[::-1])

def parsing_texts(pages:list[str]) -> list[str]:
    """
    Парсит 12 новостей с каждой страницы
    * pages: list[str] - список кодов страниц
    """
    
    texts: list[str] = [] #Текст новостей
    for page in pages:
        soup = BeautifulSoup(page, "html.parser") #Супчик
        textData = soup.find('div', class_="full-text")
        if textData is not None:
            texts.append(textData.get_text(strip=True))
    return texts

async def parsing_site(site:str = site, news_page:str = news_page, headers:dict = headers, start_page:int = start_page, last_page:int = last_page) -> tuple[list, list, list, list]:
    """
    Парсит все указанные страницы и возвращает их заголовки, ссылки, даты и тексты
    * site: str - ссылка на сайт
    * news_page: str - шаблон ссылки на страницу с 12 новостями
    * headers: dict - заголовки для запроса к сайт
    * start_page: int - номер первой страницы
    * last_page: int - номер последней страницы
    """
    
    urls = [] #Ссылки на страницы с 12 новостями
    for i in range(start_page, last_page-1, -1):
        url = site + news_page + str(i)
        urls.append(url)
        
    captions: list[str] = [] #Заголовки
    links: list[str] = [] #Ссылки
    dates: list[datetime] = [] #Даты
    texts: list[str] = [] #Текст новостей
    
    start_time = time.time()
    
    timeout = aiohttp.ClientTimeout(2400)
    session = aiohttp.ClientSession(trust_env=True, timeout=timeout)
    
    firstStep = []
    for url in urls:
        firstStep.append(asyncio.create_task(getSite(session, url, headers)))
    pages = await asyncio.gather(*firstStep)
    
    for page in pages:
        captions_n, links_n, dates_n = parsing_captions_links_dates(page, site)
        captions, links, dates = captions + captions_n, links + links_n, dates + dates_n
        
    seconds = time.time() - start_time
    minutes = seconds / 60
    print("--- Первый шаг ---")
    print("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes))
    
    start_time = time.time()
    
    secondStep = []
    for url in links:
        secondStep.append(asyncio.create_task(getSite(session, url, headers)))
    res = await asyncio.gather(*secondStep)
    await session.close()
    
    texts = parsing_texts(res)
    
    seconds = time.time() - start_time
    minutes = seconds / 60
    print("--- Второй шаг ---")
    print("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes))
    
    return (captions, links, dates, texts)

def parsing_date(page:str) -> list[datetime]:
    """
    Парсит 12 дат 
    * page: str - код страницы
    """
    
    dates: list[datetime] = [] #Даты
    soup = BeautifulSoup(page, "html.parser") #Супчик
    allNews = soup.find_all('div', class_="new-block") #Ищем все новости
    #Анализ данных
    for data in allNews:
        dateData = data.find('span', class_='date')
        if dateData is not None:
            dates.append(convertData(dateData.text))
    return dates[::-1]

async def search_last_news_12page_number(date:datetime, site:str = site, news_page:str = news_page, headers:dict = headers) -> int:
    """
    Ищет номер новости с последней датой
    * date: datetime - дата последней новости
    * site: str - ссылка на сайт
    * news_page: str - шаблон ссылки на страницу с 12 новостями
    * headers: dict - заголовки для запроса к сайт
    """
    
    number = 0
    stop = False
    
    timeout = aiohttp.ClientTimeout(2400)
    session = aiohttp.ClientSession(trust_env=True, timeout=timeout)
    
    start_page = 1
    last_page = 10
    while not stop and start_page < 30:
        urls = [] #Ссылки на страницы с 12 новостями
        for i in range(start_page, last_page+1):
            url = site + news_page + str(i)
            urls.append(url)

        start_page += 10
        last_page += 10
        
        start_time = time.time()
        
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(getSite(session, url, headers)))
        pages = await asyncio.gather(*tasks)

        for page in pages:
            dates_n = parsing_date(page)
            number += 1
            if date in dates_n:
                stop = True
                break
            
        seconds = time.time() - start_time
        minutes = seconds / 60
        print(f"--- Заход поиска {(start_page)//10} ---")
        print("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes))
        
    await session.close()
    return number

def convertData(date_raw:str) -> datetime:
    
    splt = date_raw.split(', ')
    date_str = splt[0]
    time_str = splt[1]
    
    date_str_splt = date_str.split(' ')
    day = int(date_str_splt[0])
    month = months.get(date_str_splt[1])
    year = int(date_str_splt[2])
    
    time_str_splt = time_str.split(':')
    hour = int(time_str_splt[0])
    minute = int(time_str_splt[1])
    
    return datetime(year, month, day, hour, minute)

from aiohttp_retry import RetryClient

async def getSite(session:aiohttp.ClientSession, url:str, headers:str = ''):
    retry_client = RetryClient(session)
    async with retry_client.get(url, headers=headers) as response:
        text = await response.text()
        ok = response.ok
        status = response.status
        if ok: cprint(f"{url} : {status} : {ok}", color='green')
        else: cprint(f"{url} : {status} : {ok}", color='blue')
        return (text)


    
    



