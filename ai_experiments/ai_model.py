import datetime
import pickle
import logging
import csv
import os
from enum import Enum
import string


logging.basicConfig(
    format="%(levelname)s %(asctime)s [%(filename)s:%(lineno)d]: %(message)s",
    level=logging.DEBUG,
)

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.tokenize import sent_tokenize
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.model_selection import train_test_split



nltk.download('punkt_tab')
nltk.download('stopwords')

stop_words = set(stopwords.words('russian'))
stemmer = SnowballStemmer("russian")

model = RandomForestRegressor(n_estimators=120)
vectorizer = TfidfVectorizer(stop_words=list(stop_words))

allowed_symbols = (
        string.ascii_lowercase +
        " -+%" +
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


def fit(db_path: str, boundary: float = None):
    global model, vectorizer

    df = pd.read_csv(db_path)
    df_texts = df.Text

    if boundary is None:
        boundary = (df.Value.max() + df.Value.min()) / 2
        boundary = df.Value.median()
        print("Boundary value set to ", boundary)

    # values = np.array([-1 if value < boundary else 1 for value in df.Value])

    cleared = []
    for text in df_texts:
        cleared.append(getFullClearText(text))
        # print(cleared[-1])
        # break
        # print(cleared[-1])
        # print("-----")

    vectorized = vectorizer.fit_transform(cleared)

    # for i in range(50):
    #     df_vectorized = pd.DataFrame(vectorized[i].T.todense(),
    #                   index=vectorizer.get_feature_names_out(), columns=["TF-IDF"])
    #     df_vectorized = df_vectorized.sort_values('TF-IDF', ascending=False)
    #     print(df_vectorized.head(10))

    # test_size = 0
    # random_state = 8471874

    # x_train, x_test, y_train, y_test = train_test_split(
    #     vectorized,
    #     df.Value,
    #     test_size=test_size,
    #     random_state=random_state
    # )

    # # so we can get original text but not tokenized
    # x_original_train, x_original_test, _, _ = train_test_split(
    #     df_texts,
    #     df.Value,
    #     test_size=test_size,
    #     random_state=random_state
    # )

    # x_test_texts = vectorizer.inverse_transform(x_test)
    # print(x_test)
    # print(x_test_texts)

    if "model_rf120.pkl" not in os.listdir("."):
        logging.info("Model fitting process started")

        model.fit(vectorized, df.Value)

        logging.info("Model fit")

        with open('model_rf120.pkl', 'wb') as f:
            pickle.dump(model, f)
            logging.info("Model saved")

    else:
        logging.info("Loading model...")
        with open('model_rf120.pkl', 'rb') as f:
            model = pickle.load(f)
            logging.info("Model loaded")

    # model.fit(vectorized, df.Value)

    # with open('model_rf300.pkl', 'wb') as f:
    #     pickle.dump(model, f)
    #     print("Model saved")

    # y_predict = model.predict(x_test)
    # print(model.score(x_test, y_test))

def predict(ticker: str) -> str:
    global model

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

            perspectivity = 0
            for i in range(len(news)):
                if y_predict[i] < -0.015:
                    mark = "❌"
                    perspectivity -= 1
                else:
                    mark = "✅"
                    perspectivity += 1

                sample = f"{mark} {i + 1}. [{news[i]['title']}]({news[i]['url']})"
                verdict += sample + "\n"

            overall_mark = "НЕПЕРСПЕКТИВНАЯ" if perspectivity < 0 else "ПЕРСПЕКТИВНАЯ"
            verdict += ("\n"
                        f"Общая оценка: *{overall_mark}*")

            return verdict

    except FileNotFoundError as ex:
        return f"Не нашлось новостей за последние два года для {ticker} :("


fit("../ai_experiments/database_new.csv")