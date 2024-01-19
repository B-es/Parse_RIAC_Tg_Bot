import findspark
from config import mainGlobalPath

#findspark.init(f'{mainGlobalPath}\spark\spark-3.5.0-bin-hadoop3')
findspark.init('C:\spark-3.5.0-bin-hadoop3')

import pyspark as pyspark
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import Word2Vec
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer 

def getContextSynonyms(textNews:list[str], word:str, countSynonyms:int)-> list[str]:
    
    # Открытие сессии
    conf = SparkConf()
    conf.setMaster("local").setAppName('Parse_Riac_TG_Bot')
    sc = SparkContext.getOrCreate(conf=conf)
    spark = SparkSession(sc)
    print('Запущен Spark версии', spark.version)

    # Загрузка текста новости
    text = [[text] for text in textNews]

    # Преобразование в DF
    df = spark.createDataFrame(text)
    prepared_df = df.selectExpr('_1 as text')

    # Токенизация
    tokenizer = Tokenizer(inputCol='text', outputCol='words')
    words = tokenizer.transform(prepared_df)
    words.show()

    # Фильтрация от стоп-слов
    stop_words = StopWordsRemover.loadDefaultStopWords('russian')
    remover = StopWordsRemover(inputCol = 'words', outputCol = 'filtered', stopWords = stop_words)
    filtered = remover.transform(words)
    filtered.show()

    # Построение модели Word2Vec
    word2vec = Word2Vec(minCount=2, inputCol='filtered', outputCol='result_word2vec', vectorSize=100, maxSentenceLength=1000)
    model = word2vec.fit(filtered)
    try:
        synonуms = model.findSynonymsArray(word, countSynonyms)
    except Exception as ex:
        #print(ex)
        return []
    finally:
        sc.stop()

    return synonуms


