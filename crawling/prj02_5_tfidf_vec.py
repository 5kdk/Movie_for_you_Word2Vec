import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_review_one_sentence = pd.read_csv(
    '../crawling_data/movie_review_one_sentence_2015-2021.csv')

print(df_review_one_sentence.info())

Tfidf = TfidfVectorizer()
Tfidf_matrix = Tfidf.fit_transform(df_review_one_sentence['reviews']) #모든문장의 tfidf점수를 받아서 매트릭스를 만들어줌


with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f) #tfidf 저장

mmwrite('./models/tfidf_movie_review.mtx', Tfidf_matrix) #tfidf metrix 저장