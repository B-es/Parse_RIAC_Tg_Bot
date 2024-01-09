import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parsing_site(site:str, news_page:str, headers:dict) -> tuple[list, list, list, list]:
    
    captions: list[str] = [] #Заголовки
    links: list[str] = [] #Ссылки
    dates: list[datetime] = [] #Даты
    texts: list[str] = [] #Текст новостей
    page = requests.get(news_page, headers) #Ответ сайта
    src = page.text #Html-код страницы
    soup = BeautifulSoup(src, "html.parser") #Супчик

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

    #Текст
    for link in links:
        page = requests.get(link, headers) #Ответ сайта
        src = page.text #Html-код страницы
        soup = BeautifulSoup(src, "html.parser") #Супчик
        textData = soup.find('div', class_="full-text")
        if textData is not None:
            texts.append(textData.get_text(strip=True))
            
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