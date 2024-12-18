import string

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import text2text as t2t
from nltk.tokenize import sent_tokenize
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.model_selection import train_test_split


# nltk.download('punkt_tab')
# nltk.download('stopwords')


stop_words = set(stopwords.words('russian'))
vectorizer = TfidfVectorizer(stop_words=list(stop_words))

stemmer = SnowballStemmer("russian")

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

df = pd.read_csv("database_some.csv")
# df = df.iloc[:1000]

df_texts = df.Title
# normalized to [0, 1]
values = [(value + 1) / 2 for value in df.Value]


cleared = []
for text in df_texts:
    text = text.lower()
    cleared_text = getClearText(text)
    cleared_text = replaceSymbols(cleared_text)
    cleared.append(cleared_text)

# texts = []
# for text in cleared:
#     words = word_tokenize(text)
#     words_filtered = []
#     for word in words:
#         if word in stop_words:
#             continue
#         word = stemmer.stem(word)
#         words_filtered.append(word)
#
#     text = ""
#     for word in words_filtered:
#         text += word + " "
#     # tokenized_sentences = sent_tokenize(text)
#
#     texts.append(text)

vectorized = vectorizer.fit_transform(cleared)

num_classes = 3  # Match the number of classes in the data
bin_edges = np.linspace(0, 1, num_classes + 1)  # Create bin edges
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2  # Compute bin centers

# Digitize values into bins
y_binned = np.digitize(values, bins=bin_edges, right=True) - 1  # Adjust to 0-based indexing

# Split data

random_state = 3
test_size = 0.05

x_train, x_test, y_train, y_test = train_test_split(
    vectorized,
    y_binned,
    test_size=test_size,
    random_state=random_state
)
x_original_train, x_original_test, _, _ = train_test_split(
df_texts,
    y_binned,
    test_size=test_size,
    random_state=random_state
)

# Train logistic regression
model = LogisticRegression(
    random_state=random_state,
    max_iter=100
)
model.fit(x_train, y_train)

# Predict probabilities
y_probs = model.predict_proba(x_test)

# Map probabilities back to continuous values

# print("Unique classes in y_binned:", np.unique(y_binned))
y_pred_continuous = np.dot(y_probs, bin_centers)

# Convert predictions back to original scale [-1, 1]
original_values = [2 * value - 1 for value in y_pred_continuous]

for i in range(len(y_probs)):
    print(y_probs[i], original_values[i])

# print("Continuous Predictions:", original_values)
x_test_texts = vectorizer.inverse_transform(x_test)  # List of tokenized words per row

# Combine x_test with predictions into a DataFrame
result_df = pd.DataFrame({
    "OriginalText": x_original_test,
    "VectorizedText": [" ".join(text) for text in x_test_texts],
    "Predicted_Value": original_values
})

result_df.to_csv("predicted.csv")

print(result_df)

print(model.score(x_train, y_train))
print(model.score(x_test, y_test))