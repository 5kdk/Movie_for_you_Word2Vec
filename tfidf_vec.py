"""
리뷰간의 단어를 TfidfVectorizer하고 학습시켜 저장
"""

#모듈 불러오기
import pandas as pd
from sklearn.feature_extraction.text import  TfidfVectorizer
from scipy.io import mmwrite, mmread  #mmwrite= 매트릭스 형식으로 저장하는 모듈, mmread=읽는 것
import pickle

df_review_one_sentences = pd.read_csv('./crawling_data/movie_review_one_sentence_2015_2021.csv') #데이터 불러오기
print(df_review_one_sentences.info())


#TfidfVectorizer 모델 설정
Tfidf = TfidfVectorizer(sublinear_tf=True)  #값의 스무딩(smoothing) 여부를 결정하는 파라미터
Tfidf_matrix = Tfidf.fit_transform(df_review_one_sentences['reviews'])  #리뷰 컬럼 문장들을 서로 비교해 tfidf점수를 매겨서 표로 만들어준다(단어 사전도 만들어준다)


#나중에 데이터를 추가로 넣을 때, 매겨진 tfidf점수에 적용하기 위해서 모델 tfidf와 학습시킨 tfidf_matrix를 저장해둔다
with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/tfidf_movie_review.mtx', Tfidf_matrix)  #mmwrite=매트릭스 형식을 저장하는 방식, 확장자는 mtx
