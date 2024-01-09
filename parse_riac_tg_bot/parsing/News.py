from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class News:
    number: int
    caption: str
    link: str
    date: datetime
    text: str
    
    def toInsert(self):
        return (self.caption, self.link, self.date, self.text)
    
    def __repr__(self):
        return f"Номер: {self.number}\n{'-'*100}\nЗаголовок: {self.caption}\nСсылка: {self.link}\nДата и время: {self.date}\nТекст: {self.text}\n{'-'*100}\n"