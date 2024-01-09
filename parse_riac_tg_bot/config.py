st_accept = "text/html" # говорим веб-серверу, 
                        # что хотим получить html
# имитируем подключение через браузер Mozilla на macOS
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
# формируем хеш заголовков
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

config = {
    "site": "https://riac34.ru",
    "news_page": f'/news/?PAGEN_1=',
    "headers": headers,
    "start_page": 834, #12 страниц на одной => 10008,
    "last_page": 1,
}

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