import nltk
from nltk import word_tokenize

nltk.download('punkt_tab')
text = 'Биба в бобе, боба в бабе.'
word_tokens = word_tokenize(text)
print(word_tokens)