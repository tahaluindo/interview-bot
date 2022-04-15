import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

stop_words = set(stopwords.words('english'))


#print(stop_words)
def getKeywords(answer):
    answer = answer.translate(string.punctuation)
    word_tokens = word_tokenize(answer)
    word_tokens = [word.lower() for word in word_tokens if word.isalpha()]

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return ','.join(set(filtered_sentence))
