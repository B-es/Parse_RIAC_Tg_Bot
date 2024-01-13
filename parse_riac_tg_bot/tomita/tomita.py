import subprocess
import os
from config import mainPath
from News import News

def replacePathConfig(outputName: str = 'config', rawName:str = 'rawConfig', pathName: str = 'path', toPath: str = f'{mainPath}/tomita/dependencies', path: str = f'{mainPath}/tomita', outputPath: str = f'{mainPath}/tomita/output'):
    """
    Заменяет путь у конфига для запуска из проекта
    * outputName: str - название конфига на выходе
    * rawName: str - название конфига, который содержит шаблоны для замены
    * pathName: str - название шаблона
    * toPath: str - путь, который надо вставить вместо шаблона
    * path: str - путь, где находятся конфиги
    * outputPath: str - путь, для вывода результата
    """
    
    with open(f"{path}/{rawName}.proto", 'r') as f:
        text: str = f.read()
        with open(f"{path}/{outputName}.proto", 'w') as fw:
            outputConfig = text.replace(f'{pathName}out', outputPath).replace(pathName, toPath)
            fw.write(outputConfig)

def startTomita(configName:str = 'config', path = f'{mainPath}/tomita'):
    """
    Запускает tomitaparser с указанным конфигов
    * configName: str - название конфига
    * path: str - путь, где находится конфиг и tomitaparser
    """
    
    config = f'{path}/{configName}.proto'
    if not os.path.exists(config): replacePathConfig() #Если конфига нет, создать из шаблона
    subprocess.run([f'{path}/tomitaparser.exe', config])
    
def changeInputText(text: str, path: str = f'{mainPath}/tomita/dependencies/input.txt'):
    """
    Заменяет текст в файле указанном в path
    * text: str - текст, который будет записан в файл
    * path: str - путь, где находится файл
    """
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    

from xml.dom import minidom

def readOutputXML(path: str = f'{mainPath}/tomita/output/output.xml') -> tuple[list[str], list[str]]:
    """
    Читает результат работа tomitaparser в виде xml и возвращает кортеж из випов и достопримечательностей
    * path: str - путь к файлу
    """
    vips: list[str] = []
    attractions: list[str] = []
    
    xml = minidom.parse(path)
    facts = xml.getElementsByTagName('facts')
    if facts == []: return (None, None)
    
    for child in facts[0].childNodes:
        if type(child) == minidom.Element:
            if child.nodeName == "Person":
                name = child.getElementsByTagName('Name')[0].getAttribute('val')
                surname = child.getElementsByTagName('Surname')[0].getAttribute('val')
                vips.append(f'{name} {surname}')
            else:
                attractionName = child.getElementsByTagName('Name')[0].getAttribute('val')
                attractions.append(attractionName)
                
    if vips == []: return (None, list(set(attractions)))
    elif attractions == []: return (list(set(vips)), None)
    
    return (list(set(vips)), list(set(attractions)))

def vips_attractions_collection(news_list: list[News]):
    """
    Добавляет в объекты новостей vips и attractions
    * news_list: list[News] - список новостей
    """
    
    for news in news_list:
        changeInputText(news.text)
        startTomita()
        vips, attractions = readOutputXML()
        news.vips = vips
        news.attractions = attractions