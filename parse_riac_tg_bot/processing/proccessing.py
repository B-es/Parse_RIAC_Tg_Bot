from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import NaiveBayesClassifier
from env import gigachat_creds

import re, string, random
import asyncio
from gigachat import GigaChat, GigaChatAsyncClient

async def getSummarizerText(session: GigaChatAsyncClient, newsText: str) -> str:
    try:
        response = await session.achat(f"Используя суммаризатор, максимально сократи данный текст: {newsText}")
    except Exception as e:
        print(f"Ошибка суммиризатора: {e}")
        return ''
    return response.choices[0].message.content

async def getRewriterText(session: GigaChatAsyncClient, newsText: str) -> str:
    try:
        response = await session.achat(f"Используя рерайтер, преобразуй данный текст: {newsText}")
    except Exception as e:
        print(f"Ошибка рерайтера: {e}")
        return ''
    return response.choices[0].message.content

async def getData(texts: list[str]) -> tuple[str, str]:
    with GigaChat(
            verify_ssl_certs=False,
            credentials=gigachat_creds,
            scope="GIGACHAT_API_PERS",
    ) as gigachatSession:
        tasksSummorizer = []
        tasksRewriter = []

        for text in texts:
            tasksSummorizer.append(asyncio.create_task(getSummarizerText(gigachatSession, text)))
            tasksRewriter.append(asyncio.create_task(getRewriterText(gigachatSession, text)))

        resultsSummorizer = await asyncio.gather(*tasksSummorizer)
        resultsRewriter = await asyncio.gather(*tasksRewriter)
        return (resultsSummorizer, resultsRewriter)
    
def removeNoise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[а-яА-Я]|[0-9]|[$-_@.&+#]|[!*(),]|'''
                       '(?:%[0-9а-еА-Е][0-9а-еА-Е]))+', '', token)
        token = re.sub("(@[А-Яа-я0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

from config import mainPath

def tokens(path:str):
    stop_words = stopwords.words('russian')
    texts = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            clear_line = line.replace('{"text": "', '')
            text = clear_line.removesuffix('"}\n')
            texts.append(text)
    
    cleaned_tokens_list = []

    for text in texts:
        tokens = word_tokenize(text)
        cleaned_tokens_list.append(removeNoise(tokens, stop_words))
    
    return cleaned_tokens_list

def getClassifier():
    
    path = f'{mainPath}/processing'

    positive_cleaned_tokens_list = tokens(f'{path}/positive.json')
    negative_cleaned_tokens_list = tokens(f'{path}/negative.json')

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Позитивная")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Негативная")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]

    classifier = NaiveBayesClassifier.train(train_data)
    return classifier

def getTonality(texts: list[str]) -> list[str]:
    classifier = getClassifier()
    tonals = []
    for text in texts:
        custom_tokens = removeNoise(word_tokenize(text))
        tonals.append(classifier.classify(dict([token, True] for token in custom_tokens)))
    return tonals


async def processingNews(texts: list[str]) -> tuple[list[str], list[str], list[str]]:
    tonals = getTonality(texts)
    summarizers, rewriters = await getData(texts)
    return summarizers, rewriters, tonals
