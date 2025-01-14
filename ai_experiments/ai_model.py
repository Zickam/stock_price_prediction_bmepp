import datetime
import pickle
import logging
import csv
import os
from enum import Enum
import string

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.tokenize import sent_tokenize
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.model_selection import train_test_split


nltk.download('punkt_tab')
nltk.download('stopwords')

stop_words = set(stopwords.words('russian'))
stemmer = SnowballStemmer("russian")

model = LogisticRegression(
        max_iter=1900  # 1900
    )
vectorizer = TfidfVectorizer(stop_words=list(stop_words))

allowed_symbols = (
        string.ascii_lowercase +
        " -+%.," +
        # string.digits +
        "абвгдежзийклмнопрстуфхцчшщъыьэюя"
)
def getClearText(text: str) -> str:
    cleared_text = ""
    for letter in text:
        if letter in allowed_symbols:
            cleared_text += letter

    return cleared_text

replace_dict = {
    " +": " плюс ",
    " -": " минус ",
    "%": " процент "
}
def replaceSymbols(text: str) -> str:
    new_text = text
    for key, value in replace_dict.items():
        new_text = new_text.replace(key, value)
    return new_text

def getFullClearText(text: str) -> str:
    text = text.lower()
    cleared_text = getClearText(text)
    cleared_text = replaceSymbols(cleared_text)
    return cleared_text

def fit(db_path: str):
    global model, vectorizer

    df = pd.read_csv(db_path)
    df_texts = df.Text

    values = np.array([-1 if value < 0 else 1 for value in df.Value])

    cleared = []
    for text in df_texts:
        cleared.append(getFullClearText(text))

    vectorized = vectorizer.fit_transform(cleared)

    if "model.pkl" not in os.listdir("."):
        logging.info("Model fitting process started")

        model.fit(vectorized, values)

        logging.info("Model fit")

        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)
            logging.info("Model saved")

    else:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
            logging.info("Model loaded")



class Result(Enum):
    down = -1
    no_info = 0
    up = 1

def predict(ticker: str) -> str:
    csv_path = f"../parse_experiments/recent_news/{ticker}.csv"
    try:
        with open(
                csv_path,
                mode='r',
                newline='',
                encoding='utf-8'
        ) as file:
            file.seek(0)
            reader = csv.DictReader(file)
            news = []
            predictors = []

            for i, row in enumerate(reader):
                title = row['Title']
                text = row['Text']
                time = row['Time']
                url = row['Url']

                time = datetime.datetime.strptime(time, "%d.%m.%Y, %H:%M")
                if time < datetime.datetime.now() - datetime.timedelta(days=365 * 2):
                    continue

                news.append({})
                news[i]["text"] = row["Text"]
                news[i]["url"] = row["Url"]
                news[i]["title"] = row["Title"]
                news[i]["text_cleared"] = getFullClearText(text)

                predictors.append(news[i]["text_cleared"])

            if len(news) == 0:
                return f"Не нашлось новостей за последние два года для {ticker} :("

            vectorized = vectorizer.transform(predictors)

            y_predict = model.predict(vectorized)

            logging.info(f"PREDICT {y_predict}")

            verdict = f"Оценка новостей связанных с компанией {ticker.upper()}:\n"

            for i in range(len(news)):
                match y_predict[i]:
                    case -1:
                        mark = "падение"
                    case 1:
                        mark = "рост"
                    case other:
                        mark = f"{other}: непредвиденный аргумент y_predict[i]"
                sample = f"{i + 1}. [{news[i]['title']}]({news[i]['url']}). Оценка: {mark}"
                verdict += sample + "\n"

            overall_mark = "ПАДЕНИЕ" if sum(y_predict) < 0 else "РОСТ"
            verdict += ("\n"
                        f"Общая оценка: *{overall_mark}*")

            return verdict

    except FileNotFoundError as ex:
        return f"Не нашлось новостей за последние два года для {ticker} :("


fit("../ai_experiments/database_some.csv")