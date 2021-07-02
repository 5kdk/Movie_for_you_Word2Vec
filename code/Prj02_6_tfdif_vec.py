import pickle

import pandas as pd
from scipy.io import mmwrite  # matrix 저장
from sklearn.feature_extraction.text import TfidfVectorizer

df_review_one_sentences = pd.read_csv(
    '../processing_data/movie_review_one_sentence_2015_2021.csv',
    index_col=0)
print(df_review_one_sentences.info())

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_review_one_sentences['reviews'])

# 불러온 모델 저장
with open('../models/tfidf.pickle', 'wb') as f :
    pickle.dump(Tfidf, f)

# 매트릭스 점수 저장
mmwrite('../models/tfidf_movie_review.mtx',
        Tfidf_matrix)