
"""

"""

#모듈 불러오기

import pandas as pd
from konlpy.tag import Okt
import re

#데이터 불러오기

df = pd.read_csv('crawling_data/reviews_2021.csv')
print(df.head())
"""
print(df.iloc[0, 1])  #한개의 리뷰만 가져오기
print('='*70)  #비교를 위해 줄 나누기
sentence = re.sub('[^가-힣]', '', df.iloc[0, 1])  #한글만 가져오기, 내용에서 가-힣 내용이 아니면 ''빈 문자로 변경
print(sentence)
"""
okt = Okt()

#불용어가 든 파일을 가져오기
stopwords = pd.read_csv('datasets/stopwords.csv', index_col=0)
movie_stopwords = ['영화', '배우', '감독']  #불용어에 추가해 줄 단어를 리스트로 만들기
stopwords_list = list(stopwords.stopword) + movie_stopwords  #기존 불용어단어들을 리스트로 받고 새로운 불용어 리스트도 더해 합쳐준다

#csv전체 데이터의 문장을 for문으로 전처리하기

count = 0
cleaned_sentences = []

for sentence in df.reviews:
    count += 1
    if count % 10 == 0:  #진행사항을 보기 위해 10개의 문장마다 점찍기
        print('.', end='')
    if count % 100 == 0:  #문장 100개 당 줄바꿈해주니까 점이 10개찍히면 줄바꿈 해주는 것
        print('')
    sentence = re.sub('[^가-힣 | ' ']', '', sentence)
    token = okt.pos(sentence, stem=True)  #튜플리스트 반환. 단어랑 품사랑 짝지어주는, stem=단어의 원형 반환
    # 토큰을 데이터프레임으로 만들어준다, 첫번째는 단어, 두번째는 명사인지 조사인지 등에 대한 클래스
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    # 데이터프레임안에서 조건식으로 인덱싱 가능하다(클래스가 명사, 동사, 형용사인 것만 뽑는 것)
    df_cleaned_token = df_token[(df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective')]
    words = []
    for word in df_cleaned_token['word']:  #단어를 기준으로 for문을 돌리기
        if len(word) > 1:   #한 단어는 제외한다
            if word not in stopwords_list:  #불용어 리스트에 없는 단어는 빈리스트에 추가하기
                words.append(word)
    # for문까지 끝낸 단어들을 다시 하나의 문장으로 합쳐주기
    cleaned_sentence = ' '.join(words)  
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
print(df.head())

print(df.info())

df = df[['titles', 'cleaned_sentences']]
print(df.info())
df.to_csv('./crawling_data/cleaned_review_2021.csv')