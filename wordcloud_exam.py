"""
영화를 지정해 리뷰들을 워드클라우드로 만들어보기
"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager, rc  #폰트설정
from wordcloud import WordCloud
import collections
from konlpy.tag import Okt

#폰트 설정
fontpath = './Cafe24Oneprettynight.ttf'  #폰트 경로 불러오기
font_path = './malgun.ttf'
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
mpl.font_manager._rebuild()

df = pd.read_csv('./crawling_data/one_sentence_review_2021.csv', index_col=0) #전처리 된 파일 가져오기
df.dropna(inplace=True)  #결측치 제거하기
# print(df.info())
# print(df.head())

movie_index = df[df['titles'] == '도라에몽: 스탠바이미 2 (Stand by Me Doraemon 2)'].index[0]  #지정 영화 불러오기
# print(movie_index)
print(df.reviews[movie_index])
words = df.reviews[movie_index].split(' ')  #split= 띄어쓰기로 잘린 단어들을 리스트로 만들어준다
print(words)

worddict = collections.Counter(words)  #Counter= 단어리스트 중에 각각 유니크한 단어들의 빈도를 세준다, 출력은 딕셔너리로 보이지만 딕셔너리타입은 아니다
worddict = dict(worddict)  #dict= 딕셔너리로 만들어준다
print(worddict)

stopwords = ['관객', '작품']  #필요없는 단어 제거하기

#워드클라우드 설정, generate_from_frequencies= 단어 출연빈도로 그리기
wordcloud_img = WordCloud(background_color='white', max_words=2000, font_path=fontpath)\
    .generate(df.reviews[movie_index])

#이렇게도 설정 가능하다 = 스탑워드를 직접 적어서 사용하고 싶을 때
# wordcloud_img = WordCloud(background_color='white', max_words=2000, font_path=fontpath, stopwords=stopwords)\
#     .generate_from_frequencies(worddict)

#plt그리기
plt.figure(figsize=(8,8))  #이미지 사이즈 지정
plt.imshow(wordcloud_img, interpolation="bilinear")  #interpolation= 이미지를 어떻게 처리할 지 보여준다, bilinear= 부드럽게
plt.axis('off')   # 눈금 X
plt.title(df.titles[movie_index], size=25)
plt.show()