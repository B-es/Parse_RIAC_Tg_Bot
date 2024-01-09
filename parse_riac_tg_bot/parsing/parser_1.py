import asyncio
import aiohttp
import colorama
from bs4 import BeautifulSoup
from datetime import datetime

def parsing_captions_links_dates(page:str, site:str) -> tuple[list, list, list]:
    """Парсит 12 заголовков, ссылок и дат с одной страницы"""
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
    """Парсит 12 новостей с каждой страницы"""
    texts: list[str] = [] #Текст новостей
    for page in pages:
        soup = BeautifulSoup(page, "html.parser") #Супчик
        textData = soup.find('div', class_="full-text")
        if textData is not None:
            texts.append(textData.get_text(strip=True))
    return texts

async def parsing_site(site:str, news_page:str, headers:dict, start_page:int = 834, last_page:int = 1) -> tuple[list, list, list, list]:
    
    urls = [] #Ссылки на страницы с 12 новостями
    for i in range(start_page, last_page-1, -1):
        url = site + news_page + str(i)
        urls.append(url)
        i -= 1
        
    captions: list[str] = [] #Заголовки
    links: list[str] = [] #Ссылки
    dates: list[datetime] = [] #Даты
    texts: list[str] = [] #Текст новостей
    
    import time
    start_time = time.time()
    
    timeout = aiohttp.ClientTimeout(2400)
    session = aiohttp.ClientSession(trust_env=True, timeout=timeout)
    
    firstStep = []
    for url in urls:
        firstStep.append(asyncio.create_task(getSite(session, url, headers)))
    pages = await asyncio.gather(*firstStep)
    #await session.close()
    
    for page in pages:
        captions_n, links_n, dates_n = parsing_captions_links_dates(page, site)
        captions, links, dates = captions + captions_n, links + links_n, dates + dates_n
        
    seconds = time.time() - start_time
    minutes = seconds / 60
    print("--- Первый шаг ---")
    print("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes))
    
    start_time = time.time()
    
    #session = aiohttp.ClientSession(trust_env=True, timeout=timeout)
    
    secondStep = []
    for url in links:
        secondStep.append(asyncio.create_task(getSite(session, url, headers)))
    res = await asyncio.gather(*secondStep)
    await session.close()
    
    texts = parsing_texts(res)
    print(len(texts))
    
    seconds = time.time() - start_time
    minutes = seconds / 60
    print("--- Второй шаг ---")
    print("--- %s секунд ---\n--- %s минут ---" % (seconds, minutes))
    
    return (captions, links, dates, texts)


from config import months

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
        if ok: print(colorama.Fore.GREEN + f"{url} : {status} : {ok}")
        else: print(colorama.Fore.BLUE + f"{url} : {status} : {ok}")
        return (text)


    
    



