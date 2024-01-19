# Компьютерная лингвистика.

## Контрольная работа. Вариант [№6](https://riac34.ru)

### Задание №1: Распарсить сайт из списка согласно номеру задания. Краулер должен считывать новостную ленту с первой страницы сайта или из rss-ленты. Периодичность повторения парсинга устанавливается пользователем.
- Данные заполняются в БД (не менее 10 тыс. новостей). Обязательные распарсенные поля для текста новости:
- Название новости
- Дата новости
- Ссылка на новость
- Текст новости
- Данная информация отображается в разработанном чат-боте для Telegram. Новости появляются в конце списка согласно дате публикации на сайте (самые новые - последние).

***

### Задание №2: Выявить с помощью Томита-парсера упоминание в тексте vip-персон Волгоградской области и достопримечательностей. 
- Дополнить информацию о новости в чат-боте Telegram следующими полями:
- [VIP-персоны](https://xn--b1ats.xn--80asehdb/feed/obshchestvo/andrey-bocharov-vozglavil-top-100-vliyatelnykh-lyudey-volgogradskoy-oblasti-7478520448.html);
- [Достопримечательности](https://www.kp.ru/russia/volgograd/dostoprimechatelnosti/);
- С помощью Spark MlLib и модели word2vec провести анализ на всем объеме новостных статей из БД. Для любого введенного слова определить контекстные синонимы и слова, с которыми они упоминались в тексте.

***

### Задание №3: Подключить [Суммаризатор](https://developers.sber.ru/portal/products/summarizer) для создания аннотации новости. Подключить [Рерайтер](https://developers.sber.ru/portal/products/rewriter) для переписывания текста новости
- Осуществить выявление тональности высказываний по отношению к текстам новостей с упоминанием vip-персон Волгоградской области и достопримечательностей.
- Дополнить информацию о новости в чат-боте Telegram следующими полями:
- Аннотация
- Переписанная новость
- Оценка тональности новости

***

### [Бот](https://t.me/priac_bot), содержащий базу данных из новостей с сайта [РИАЦ](https://riac34.ru)

***

### Весь текст обработан с помощью лингвистических инструментов

***

### Стек технологий

#### Инструменты: 
- ___ЯП: Python 3.11.2___
- ___БД: SQLite___
- ___Интрефейс: Telegram Bot___
- ___Среда разработки: Visual Studio Code___
- ___Фреймворк Apache Spark 3.5.0___

#### Библиотеки:
- _aiohttp = "^3.9.1"_
- _aiohttp-retry = "^2.8.3"_
- _bs4 = "^0.0.1"_
- _pytelegrambotapi = "^4.14.1"_
- _gigachat = "^0.1.13"_
- _nltk = "^3.8.1"_
- _pyspark = "^3.5.0"_
- _apscheduler = "^3.10.4"_


<h2 align="center">
Команда
</h2>
<h3 align="center">
> Васильев Иван Сергеевич <span style="color:red">(Задание №1)</span>
</h3>
<p align="center">
    <a href="https://github.com/B-es"><img src="https://avatars.githubusercontent.com/u/104147126?v=4" alt="tankistqazwsx" width="50" height="50"> </a>
</p>


<h3 align="center">
> Ваганов Владислав Игоревич <span style="color:red">(Задание №2)</span>
</h3>
<p align="center">
    <a href="https://github.com/VladislavGrom1"><img src="https://avatars.githubusercontent.com/u/108086934?v=4" alt="Kolyamba-mamba" width="50" height="50"> </a>
</p>


<h3 align="center">
> Мухин Дмитрий Андреевич <span style="color:red">(Задание №3)</span>
</h3>
<p align="center">
    <a href="https://github.com/oxordth"><img src="https://avatars.githubusercontent.com/u/101668918?v=4" alt="Kolyamba-mamba" width="50" height="50"> </a>
</p>
