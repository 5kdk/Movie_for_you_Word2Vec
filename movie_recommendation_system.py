"""
영화 추천 시스템 만들기
"""

import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
import pickle

#데이터 불러오기
df_review_one_sentence = pd.read_csv('./crawling_data/movie_review_one_sentence_2015_2021.csv')


ls = ['겨울왕국', '라이온킹', '알라딘']
print(enumerate(ls))
for idx, i in enumerate(ls):
    if i == '라이온킹':
        print(idx)

exit()

#저장해놓은 tfidf, tfidf_matrix 불러오기
Tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# 추천 함수 생성
def getRcommendation(cosine_sim):
    # movie_idx와 전체 martix의 cosine 유사도에 해당하는 값과 index list로 반환
    #cosine_sime = shape: (1, len(Tfidf_matrix))라서 [[~~~~]] 이런 형식
    simScore = list(enumerate(cosine_sim[-1]))  #코사인 유사도로 나온 영화들을 -1로 정렬시키고 인덱스를 주기, enumerate=인덱스가 붙는다
    simScore = sorted(simScore, key=lambda x:x[-1], reverse=True)  #코사인 유사도 값이 큰 순으로 정렬이 된다
    simScore = simScore[1:11]  #10개만 인덱싱하기, 0은 지정 영화 자체(movie_idx)라서 뺀 것
    movieidx = [i[0] for i in simScore]  #10개의 영화 컴럼의 0번째인 인덱스만 가져와 movie_idx에 저장
    recMovieList = df_review_one_sentence.iloc[movieidx]  #영화들의 해당 인덱스를 원문에서 찾아서 반환하기
    return recMovieList

#영화 제목이 기생충인 것만 찾아서 인덱싱해주기, 한 줄밖에 없지만 리스트로 오기 때문에 index[0] 해야 한다
movie_idx = df_review_one_sentence[df_review_one_sentence['titles'] == '라이온 킹 (The Lion King)'].index[0]

#movie_idx = 127  #임의의 숫자를 지정해서 영화를 선택해도 된다(영화 제목이 아닌)
#print(df_review_one_sentence.iloc[movie_idx, 0])  #movie_idx의 row에서 0번 컬럼이 title 이라서 이렇게 찍으면 영화 이름을 알 수 있다

#코사인 유사도 확인하기
cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)  #점수 표에서 지정시킨 영화와 전체 영화를 비교해 유사한 영화를 선택
recommendation = getRcommendation(cosine_sim)  #유사한 영화 10개를 추천
print(recommendation)  #추천된 영화 확인