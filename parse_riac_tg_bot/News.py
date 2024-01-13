from dataclasses import dataclass
from datetime import datetime
from typing import Optional

#TODO: Добавить конвертор для полей, дабы хранить в базе данных


@dataclass()
class News:
    number: Optional[int] = None 
    caption: Optional[str] = None
    link: Optional[str] = None
    date: Optional[datetime] = None
    text: Optional[str] = None
    vips: Optional[list[str]] = None #Нужно конвертировать в строку для хранения в базе данных
    attractions: Optional[list[str]] = None #Нужно конвертировать в строку для хранения в базе данных
    annotation: Optional[str] = None 
    rewrite: Optional[str] = None 
    tonality: Optional[list[str]] = None #Нужно конвертировать в строку для хранения в базе данных
    
    def toInsert(self) -> tuple:
        """Функция возвращает кортеж данных для добавления"""
        vips = []
        attractions = []
        tonality = []
        if self.vips != None: vips = self.vips
        if self.attractions != None: attractions = self.attractions
        if self.tonality != None: tonality = self.tonality
        
        return (self.caption, self.link, self.date, self.text, ','.join(vips), ','.join(attractions),\
                self.annotation, self.rewrite, ','.join(tonality))
        
    def toUpdate(self) -> tuple:
        """Функция возвращает кортеж данных для обновления"""
        return (self.number, *self.toInsert())
    
    def setData(self, data:tuple):
        """Установить данные классу"""
        self.number = data[0]
        self.caption = data[1]
        self.link = data[2]
        self.date = data[3]
        self.text = data[4]
        self.vips = None if data[5] == '' or data[5] == None else data[5].split(',')
        self.attractions = None if data[6] == '' or data[6] == None else data[6].split(',')
        self.annotation = data[7]
        self.rewrite = data[8]
        self.tonality = None if data[9] == '' or data[9] == None else data[9].split(',')
    
    def __repr__(self):
        return f"Номер: {self.number}\n{'-'*100}\nЗаголовок: {self.caption}\nСсылка: {self.link}\nДата и время: {self.date}\nТекст: {self.text}\n{'-'*100}\n" +\
        f"VIP-персоны: {self.vips}\nДостопримечательности: {self.attractions}\n\nАннотация: {self.annotation}\n\nПерезапись: {self.rewrite}\n\nТональность: {self.tonality}\n{'-'*100}\n"