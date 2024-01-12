import subprocess
import os
from config import mainPath

def replacePathConfig(outputName: str = 'config', rawName:str = 'rawConfig', pathName: str = 'path', toPath: str = f'{mainPath}/tomita/dependencies', path: str = f'{mainPath}/tomita'):
    """
    Заменяет путь у конфига для запуска из проекта
    * outputName: str - название конфига на выходе
    * rawName: str - название конфига, который содержит шаблоны для замены
    * pathName: str - название шаблона
    * toPath: str - путь, который надо вставить вместо шаблона
    * path: str путь, где находятся конфиги
    """
    
    with open(f"{path}/{rawName}.proto", 'r') as f:
        text: str = f.read()
        with open(f"{path}/{outputName}.proto", 'w') as fw:
            fw.write(text.replace(pathName, toPath))

def startTomita(configName:str = 'config', path = f'{mainPath}/tomita'):
    """
    Запускает tomitaparser с указанным конфигов
    * configName: str - название конфига
    * path: str - путь, где находится конфиг и tomitaparser
    """
    
    config = f'{path}/{configName}.proto'
    if not os.path.exists(config): replacePathConfig()
    subprocess.run([f'{path}/tomitaparser.exe', config])