import pandas as pd
from gensim.models import Word2Vec

review_word = pd.read_csv(
    './crawling_data/movie_review_2015-2021.csv'
)

print(review_word.info())

cleaned_token_review = list(review_word['cleaned_sentences'])
print(len(cleaned_token_review))
cleaned_tokens = []
count = 0
for sentence in cleaned_token_review:
    token = sentence.split(' ')
    cleaned_tokens.append(token)

print(len(cleaned_tokens))
#print(cleaned_token_review[0])
#print(cleaned_tokens[0]) # cleaned_tokens의 index[0]을 okt에서 단어로 토크나이즈 한것과 같다.

# embedding_model = Word2Vec(cleaned_tokens, vector_size=100,
#                            window=4, min_count=20,
#                            workers=4, epochs=100, sg=1)
# embedding_model.save('./crawling/models/word2VecModel_2015_2021.model')

embedding_model = Word2Vec.load("./models/word2VecModel_2015_2021.model")
print(embedding_model.wv.vocab.keys())
print(len(embedding_model.wv.key_to_index()))