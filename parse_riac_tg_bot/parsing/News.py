from dataclasses import dataclass
from datetime import datetime
from typing import Optional

#TODO: Добавить поля
# VIP-персоны
# Достопримечательности
# Аннотация
# Переписанная новость
# Оценка тональности новости

@dataclass()
class News:
    number: int 
    caption: str
    link: str
    date: datetime
    text: str
    vips: Optional[list[str]] = None
    attractions: Optional[list[str]] = None
    annotation: Optional[str] = None
    rewrite: Optional[str] = None
    tonality: Optional[list[str]] = None
    
    def toInsert(self):
        return (self.caption, self.link, self.date, self.text)
    
    def __repr__(self):
        return f"Номер: {self.number}\n{'-'*100}\nЗаголовок: {self.caption}\nСсылка: {self.link}\nДата и время: {self.date}\nТекст: {self.text}\n{'-'*100}\n" +\
        f"VIP-персоны: {self.vips}\nДостопримечательности: {self.attractions}\n\nАннотация: {self.annotation}\n\nПерезапись: {self.rewrite}\n\nТональность: {self.tonality}"
        
news = News(1, "3", "123", datetime.now(), "123")

print(news)