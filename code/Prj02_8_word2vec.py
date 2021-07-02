import pandas as pd
from gensim.models import Word2Vec

review_word = pd.read_csv(
    '../processing_data/movie_review_2015_2021.csv',
    index_col=0)

print(review_word.info())
cleaned_token_review = list(review_word['cleaned_sentences'])
print(len(cleaned_token_review))
cleaned_tokens = []
count = 0
for sentence in cleaned_token_review:
    token = sentence.split(' ')
    cleaned_tokens.append(token)
# print(len(cleaned_tokens))
# print(cleaned_token_review[0])
# print(cleaned_tokens[0])
embedding_model = Word2Vec(
    cleaned_tokens, vector_size=100, window=4, min_count=20, workers=12, epochs=100, sg=1
) 
# vector_size: 차원 수
# windows: 앞 뒤로 고려하는 단어의 수
# workers: 사용 cpu 수
# min_count: 단어의 최소 등장 횟수
embedding_model.save('../models/word2VecModel_2015_2021.model')
# print(embedding_model.wv.vocab.keys())
# print(len(embedding_model.wv.vocab.keys())) # 단어 사전에 몇개가있는지