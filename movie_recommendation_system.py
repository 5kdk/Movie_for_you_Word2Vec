import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
import pickle


df_review_one_sentence = pd.read_csv(
    './crawling_data/movie_review_one_sentence_2015-2021.csv'
)
Tfidf_metrix = mmread('./crawling/models/tfidf_movie_review.mtx').tocsr()
with open('./crawling/models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)


def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[1:10]
    movieidx = [i[0] for i in simScore]
    recMovieList = df_review_one_sentence.iloc[movieidx] #가장 유사한 영화 10개 받기
    return recMovieList


movie_idx =df_review_one_sentence[
    df_review_one_sentence[
        'titles']=='기생충 (PARASITE)'].index[0]
#존 윅 3: 파라벨룸 (John Wick: Chapter 3 - Parabellum)
#말레피센트 2 (Maleficent: Mistress of Evil)


#movie_idx = 127
#print(df_review_one_sentence.iloc[movie_idx,0]) # 127번 영화의 제목 찾기
cosine_sim = linear_kernel(Tfidf_metrix[movie_idx],
                           Tfidf_metrix)     #코사인 유사도
recommendation = getRecommendation(cosine_sim)
print(recommendation)