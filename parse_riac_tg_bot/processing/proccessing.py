from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
from env import gigachat_creds

import re, string, random
import asyncio
from gigachat import GigaChat, GigaChatAsyncClient
import codecs

async def getSummarizerText(session: GigaChatAsyncClient, newsText: str) -> str:
    response = await session.achat(f"Используя суммаризатор, максимально сократи данный текст: {newsText}")
    return response.choices[0].message.content

async def getRewriterText(session: GigaChatAsyncClient, newsText: str) -> str:
    response = await session.achat(f"Используя рерайтер, преобразуй данный текст: {newsText}")
    return response.choices[0].message.content

async def getDataSummarizerAndRewriter(texts: list[str]) -> tuple[str, str]:
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
    
def remove_noise(tweet_tokens, stop_words = ()):

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

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

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
        cleaned_tokens_list.append(remove_noise(tokens, stop_words))
    
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
        custom_tokens = remove_noise(word_tokenize(text))
        tonals.append(classifier.classify(dict([token, True] for token in custom_tokens)))
    return tonals


async def processing_news(texts: list[str]) -> tuple[list[str], list[str], list[str]]:
    tonals = getTonality(texts)
    summarizers, rewriters = await getDataSummarizerAndRewriter(texts)
    return summarizers, rewriters, tonals
