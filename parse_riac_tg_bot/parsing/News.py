from dataclasses import dataclass
from datetime import datetime

@dataclass
class News:
    caption: str
    link: str
    date: datetime
    text: str