st_accept = "text/html" #Для получения Html

#Имитируем подключение через браузер Mozilla на macOS
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"

#Формируем хеш заголовки
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

#Конфиг с основными данными о сайте
config = {
    "site": "https://riac34.ru",
    "news_page": f'/news/?PAGEN_1=',
    "headers": headers,
    "start_page": 834, #12 страниц на одной => 10008,
    "last_page": 1,
}

#Словарь для замены месяцев на числа
months = {  
        'января': 1, 
        'февраля': 2, 
        'марта': 3, 
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7, 
        'августа': 8, 
        'сентября': 9, 
        'октября': 10, 
        'ноября': 11, 
        'декабря': 12
        }

mainPath = 'parse_riac_tg_bot' #Главный путь проекта