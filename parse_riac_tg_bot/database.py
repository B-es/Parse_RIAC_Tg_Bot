import sqlite3

#TODO: Добавить поля
# VIP-персоны
# Достопримечательности
# Аннотация
# Переписанная новость
# Оценка тональности новости

class Database():
    """Класс для взаимодействия с базой данных"""
    
    def __init__(self) -> None:
        self.openConnection()
        # Создаем таблицу News
        sql_table = '''
        CREATE TABLE IF NOT EXISTS News (
        id INTEGER PRIMARY KEY,
        caption TEXT NOT NULL,
        link TEXT NOT NULL,
        date TIMESTAMP NOT NULL,
        text TEXT NOT NULL)
        '''
        self.executeSql(sql_table)
        self.closeConnection()
    
    def openConnection(self):
        """Открыть соединение"""
        
        self.connection = sqlite3.connect('news.db')
    
    def closeConnection(self):
        """Закрыть соединение"""
        
        self.connection.close()
        
    def executeSql(self, sql: str, parameters: tuple = None):
        """
        Исполнить sql-запрос
        * sql: str - sql-запрос с шаблоном (?,?..,?)
        * parameters: tuple - данные для отправки
        """
        
        cursor = self.connection.cursor()
        cursor.execute(sql) if parameters is None else cursor.execute(sql, parameters)
        cursor.close()
        self.connection.commit()
        
    def add(self, news:tuple):
        """
        Добавить строку в базу данных
        * news: tuple - новость
        """
        
        sql = '''INSERT INTO News(caption, link, date, text) VALUES(?, ?, ?, ?)'''
        self.executeSql(sql, news)
    
    def addOne(self, news:tuple):
        """
        Добавляет одну строку в базу данных
        * news: tuple - новость
        """
        
        self.openConnection()
        self.add(news)
        self.closeConnection()
        
    def addList(self, list_news:list[tuple]):
        """
        Добавляет список в базу данных
        * list_news: list[tuple] - новости
        """
        
        self.openConnection()
        for news in list_news:
            self.add(news)
        self.closeConnection()
        
    def getNewsCount(self):
        """Получить количество записей в базе данных"""
        
        self.openConnection()
        sql = "SELECT COUNT(*) FROM News"
        cursor = self.connection.cursor()
        res = cursor.execute(sql)
        count = res.fetchall()[0][0]
        self.closeConnection()
        return count

    def getList(self):
        """Получить все записи из базы данных"""
        
        self.openConnection()
        sql = "SELECT * FROM News"
        cursor = self.connection.cursor()
        res = cursor.execute(sql)
        list = res.fetchall()
        self.closeConnection()
        return list