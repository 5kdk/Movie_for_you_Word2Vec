import pandas as pd
from konlpy.tag import Okt
import re
from multiprocessing import Pool
from tqdm import tqdm

tqdm.pandas()

okt = Okt()
df = pd.read_csv('../crawling_data/reviews_2020.csv')
df.head(20)

stopwords = pd.read_csv('../datasets/stopwords.csv', index_col=0)
#print(stopwords)

# 또 다른 불용어 추가
movie_stopwords = ['영화', '배우', '감독']
stopwords_list = list(stopwords.stopword) + movie_stopwords

cleaned_sentences = []
for sentence in tqdm(df.reviews):
    sentence = re.sub('[^가-힣 ]', '', sentence)
    token = okt.pos(sentence, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_cleaned_token = df_token[
        (df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective')]
    words = [word for word in df_cleaned_token['word'] if word not in stopwords_list and len(word) > 1]
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
print(df.head())

print(df.info())

df = df[['titles', 'cleaned_sentences']]
print(df.info())
df.to_csv('./cleaned_review_2020.csv')
# tqdm 없을시 (강사님 포문)

# count = 0
# cleaned_sentences = []
# for sentence in df.reviews:
#     # 진행 상황 확인
#     count + - 1
#     if count % 10 == 0:
#         print('.', end='')
#     if count % 100 == 0:
#         print('')
#
#     sentence = re.sub('[^가-힣 ]', '', sentence)
#     token = okt.pos(sentence, stem=True)
#     df_token = pd.DataFrame(token, columns=['word', 'class'])
#     df_cleaned_token = df_token[
#         (df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective')]
#     words = []
#     for word in df_cleaned_token['word']:
#         if len(word) > 1:
#             if word not in stopwords_list:
#                 words.append(word)
#
#     # words = [word for word in df_cleaned_token['word'] if word not in stopwords_list and len(word) > 1]
#     cleaned_sentence = ' '.join(words)
#     cleaned_sentences.append(cleaned_sentence)
#
# df['cleaned_sentences'] = cleaned_sentences
# print(df.head())