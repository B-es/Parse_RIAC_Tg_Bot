import sqlite3

class Database():
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
        self.connection = sqlite3.connect('news.db')
    
    def closeConnection(self):
        self.connection.close()
        
    def executeSql(self, sql, parameters = None):
        cursor = self.connection.cursor()
        cursor.execute(sql) if parameters is None else cursor.execute(sql, parameters)
        cursor.close()
        self.connection.commit()
        
    def add(self, news:tuple):
        sql = '''INSERT INTO News(caption, link, date, text) VALUES(?, ?, ?, ?)'''
        self.executeSql(sql, news)
    
    def addOne(self, news:tuple):
        self.openConnection()
        self.add(news)
        self.closeConnection()
        
    def addList(self, list_news:list[tuple]):
        self.openConnection()
        for news in list_news:
            self.add(news)
        self.closeConnection()
        
    def getNewsCount(self):
        self.openConnection()
        sql = "SELECT COUNT(*) FROM News"
        cursor = self.connection.cursor()
        res = cursor.execute(sql)
        count = res.fetchall()[0][0]
        self.closeConnection()
        return count

    def getList(self):
        self.openConnection()
        sql = "SELECT * FROM News"
        cursor = self.connection.cursor()
        res = cursor.execute(sql)
        list = res.fetchall()
        self.closeConnection()
        return list