import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
import pickle
from gensim.models import Word2Vec

# 데이터 불러오기
df_review_one_sentence = pd.read_csv('../processing_data/movie_review_one_sentence_2015_2021.csv')

Tfidf_matrix = mmread('../models/tfidf_movie_review.mtx').tocsr()
with open('../models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# 추천 함수 생성
def getRecommendation(cosine_sim):
    # movie_idx와 전체 martix의 cosine 유사도에 해당하는 값과 index list로 반환
    simScore = list(enumerate(cosine_sim[-1]))
    # 유사도의 내림차순으로 정렬
    simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
    # 가장 유사한 상위 10개 영화
    simScore = simScore[1:11]
    # 10개 영화의 index
    movieidx = [i[0] for i in simScore]
    recMovieList = df_review_one_sentence.iloc[movieidx]
    return recMovieList

#영화 제목이 찾기, 리스트 인덱싱 (index[0])
movie_idx = df_review_one_sentence[
    df_review_one_sentence['titles'] == "존 윅 3: 파라벨룸 (John Wick: Chapter 3 - Parabellum)"
    ].index[0]

#movie_idx = 127
#print(df_review_one_sentence.iloc[movie_idx, 0])


# cosine_sim = linear_kernel(Tfidf_matrix[movie_idx],
#                            Tfidf_matrix)
# # shape: (1, len(Tfidf_matrix))
# # 유사한 영화 10개를 추천
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)


embedding_model = Word2Vec.load('../models/word2VecModel_2015_2021.model')
key_word = "전율"
sentence = [key_word] * 10
if key_word in embedding_model.wv.key_to_index:
    sim_word = embedding_model.wv.most_similar(key_word, topn=10)
    labels = []
    for label, _ in sim_word:
        labels.append(label)
    print(labels)
    # 가장 유사한 단어를 많이 저장 ex) ['소름', '돋다', '온몸', '벅차오르다', '흥분', '짜릿하다', '웅장', '압도', '감동', '카타르']
    for i, word in enumerate(labels):
        sentence += [word] * (9 - i)

# 유사한 단어를 조합한 문장
sentence = " ".join(sentence)
print(sentence)

sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation['titles'])