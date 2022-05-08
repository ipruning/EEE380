# text-to-speech (TTS)

# 负责计算语言与预设语句的相似度；
# 预设语句库；
# 相似度计算；

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

try:
    input_sentence = r.recognize_vosk(audio)
    print("")
    print("System    : An apple a day keeps the doctor away")
    print(f"User Input: {input_sentence}")
    # print("User Input: An banana a day keeps the doctor away")
    print("")
except sr.UnknownValueError:
    print("Vosk could not understand audio")
except sr.RequestError as e:
    print("Vosk error; {0}".format(e))

print("Text similarity:")

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    # "I'd like an apple",
    # "An apple a day keeps the doctor away",
    "An apple a day keeps the doctor away",
    # "Never compare an apple to an apple, think different",
    str(input_sentence),
    # "An banana a day keeps the doctor away",
]

input_doc = "An apple a day keeps the doctor away"
input_idx = corpus.index(input_doc)

vect = TfidfVectorizer(min_df=1, stop_words="english")
tfidf = vect.fit_transform(corpus)
pairwise_similarity = tfidf * tfidf.T

print(pairwise_similarity.A)

arr = pairwise_similarity.toarray()
np.fill_diagonal(arr, np.nan)
result_idx = np.nanargmax(arr[input_idx])

# print("User Input:", corpus[result_idx])
