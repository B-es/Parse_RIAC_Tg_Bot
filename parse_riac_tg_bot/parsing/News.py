from dataclasses import dataclass
from datetime import datetime

@dataclass
class News:
    number: int
    caption: str
    link: str
    date: datetime
    text: str
    
    
    def toInsert(self):
        return (self.caption, self.link, self.date, self.text)
    
    def print(self):
        print(f"Number: {self.number}\n{'-'*100}\nCaption: {self.caption}\nLink: {self.link}\nDate: {self.date}\nText: {self.text}\n{'-'*100}")