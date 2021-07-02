import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
import pickle
from gensim.models import Word2Vec


df_review_one_sentence = pd.read_csv(
    './crawling_data/movie_review_one_sentence_2015-2021.csv'
)



ls=['겨울왕국','라이온킹','알라딘']
print(list(enumerate(ls)))
print(list(enumerate(ls[-1])))
#exit()
Tfidf_metrix = mmread('./crawling/models/tfidf_movie_review.mtx').tocsr()
with open('./crawling/models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)


def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True) #유사도가 가장 높은 것으로 정렬
    simScore = simScore[1:11] #자기 자신 빼고 유사도가 가장 높은 10개 추출
    movieidx = [i[0] for i in simScore]
    recMovieList = df_review_one_sentence.iloc[movieidx] #가장 유사한 영화 10개 받기
    return recMovieList


# movie_idx =df_review_one_sentence[
#     df_review_one_sentence[
#         'titles']=='존 윅 3: 파라벨룸 (John Wick: Chapter 3 - Parabellum)'].index[0]
# #존 윅 3: 파라벨룸 (John Wick: Chapter 3 - Parabellum)
# #말레피센트 2 (Maleficent: Mistress of Evil)
# #기생충 (PARASITE)
#
#
# #movie_idx = 127
# #print(df_review_one_sentence.iloc[movie_idx,0]) # 127번 영화의 제목 찾기
# cosine_sim = linear_kernel(Tfidf_metrix[movie_idx],
#                            Tfidf_metrix)     #코사인 유사도
# print(list(enumerate(cosine_sim)))
# print(list(enumerate(cosine_sim[-1])))
# recommendation = getRecommendation(cosine_sim)
# print(recommendation.iloc[:,0]) #영화 제목만

embedding_model = Word2Vec.load("./models/word2VecModel_2015_2021.model")
key_word = '겨울'
sentence = [key_word] * 10
if key_word in embedding_model.wv.index_to_key:
    sim_word = embedding_model.wv.most_similar(key_word, topn=10)
    labels = []
    for label, _ in sim_word:
        labels.append(label)
    print(labels)
    for i, word in enumerate(labels):
        sentence += [word] * (9 - i)

sentence = ' '.join(sentence)
print(sentence)

#겨울이라는 키워드를 입력했을때 추천되는 영화 10개
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec,
                           Tfidf_metrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation.iloc[:,0])