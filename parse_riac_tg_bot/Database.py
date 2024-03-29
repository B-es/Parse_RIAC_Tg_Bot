import sqlite3
from typing import Any

class Database():
    """Класс для взаимодействия с базой данных"""
    
    def __init__(self, dbName:str = 'news.db') -> None:
        self.dbName = dbName
        self.openConnection()
        # Создаем таблицу News
        sql_table = '''
        CREATE TABLE IF NOT EXISTS News (
        id INTEGER PRIMARY KEY,
        caption TEXT NOT NULL,
        link TEXT NOT NULL,
        date TIMESTAMP NOT NULL,
        text TEXT NOT NULL,
        vips TEXT,
        attractions TEXT,
        annotation TEXT,
        rewrite TEXT,
        tonality TEXT)
        '''
        self.executeSql(sql_table)
        self.closeConnection()
    
    def openConnection(self):
        """Открыть соединение"""
        
        self.connection = sqlite3.connect(self.dbName)
    
    def closeConnection(self):
        """Закрыть соединение"""
        
        self.connection.close()
        
    def executeSql(self, sql: str, parameters: tuple = None) -> Any:
        """
        Исполнить sql-запрос
        * sql: str - sql-запрос с шаблоном (?,?..,?)
        * parameters: tuple - данные для отправки
        """
        
        cursor = self.connection.cursor()
        res = cursor.execute(sql) if parameters is None else cursor.execute(sql, parameters)
        cursor.close()
        self.connection.commit()
        return res
    
    def update(self, item: tuple):
        """
        Обновить строку в базу данных
        * item: tuple - строка
        """
        
        sql = '''UPDATE News SET caption = ?, link = ?, date = ?, text = ?, vips = ?, attractions = ?, annotation = ?, rewrite = ?, tonality = ? WHERE id = ?'''
        self.executeSql(sql, item)
        
    def updateOne(self, item:tuple):
        """
        Обновляем одну строку в базу данных
        * item: tuple - строка
        """
        
        self.openConnection()
        self.update(item)
        self.closeConnection()
        
    def updateList(self, list_item:list[tuple]):
        """
        Обновляем список в базу данных
        * list_item: list[tuple] - список данных
        """

        self.openConnection()
        for item in list_item:
            self.update(item)
        self.closeConnection()
        
    def add(self, item:tuple):
        """
        Добавить строку в базу данных
        * item: tuple - строка
        """
        
        sql = '''INSERT INTO News(caption, link, date, text) VALUES(?, ?, ?, ?)'''
        self.executeSql(sql, item)
    
    def addOne(self, item:tuple):
        """
        Добавляет одну строку в базу данных
        * item: tuple - строка
        """
        
        self.openConnection()
        self.add(item)
        self.closeConnection()
        
    def addList(self, list_item:list[tuple]):
        """
        Добавляет список в базу данных
        * list_item: list[tuple] - список данных
        """

        self.openConnection()
        for item in list_item:
            self.add(item)
        self.closeConnection()
        
    def getNewsCount(self) -> int:
        """Получить количество записей в базе данных"""
        
        self.openConnection()
        sql = "SELECT COUNT(*) FROM News"
        cursor = self.connection.cursor()
        res = cursor.execute(sql)
        count = res.fetchall()[0][0]
        self.closeConnection()
        return count

    def getList(self) -> list[tuple]:
        """Получить все записи из базы данных"""
        
        self.openConnection()
        sql = "SELECT * FROM News"
        cursor = self.connection.cursor()
        res = cursor.execute(sql)
        list = res.fetchall()
        self.closeConnection()
        return list
    
    def getLast(self) -> tuple:
        """Получить последнюю запись из базы данных"""
        self.openConnection()
        sql = "SELECT * FROM News ORDER BY ID DESC LIMIT 1"
        cursor = self.connection.cursor()
        res = cursor.execute(sql)
        note = res.fetchone()
        self.closeConnection()
        return note
    