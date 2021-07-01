import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from konlpy.tag import Okt
import matplotlib as mpl
from matplotlib import font_manager, rc

# 워드 클라우드 폰트 path
cloudfontpath = '../font/Jalnan.ttf'

# plt 한글 출력
font_path = "C:/Windows/Fonts/Malgun.TTF"
font = font_manager.FontProperties(fname=font_path).get_name() 
rc('font', family=font)

df = pd.read_csv('../crawling_data/cleaned_review_2018.csv', index_col=0)
df.dropna(inplace=True)
print(df.info())
print(df.head(20))

movie_index = df[df["titles"] == "극장판 포켓몬스터 모두의 이야기 (Pokemon the Movie: The Power of Us)"].index[11] #지정 영화의 인덱스 번호를 보고 싶을 때

# print(movie_index)
print(df.cleaned_sentences[movie_index])
words = df.cleaned_sentences[movie_index].split(' ')
print(words)

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

# wordcloud_img = WordCloud(
#     background_color="White", max_words=2000, font_path=cloudfontpath
#     ).generate_from_frequencies(worddict)
wordcloud_img = WordCloud(font_path=cloudfontpath,\
                          background_color = "white",\
                          width = 1000,\
                          height = 1000,\
                          max_words=100,\
                          max_font_size=300).generate_from_frequencies(worddict)
plt.figure(figsize=(10, 10))
plt.imshow(wordcloud_img, interpolation="bilinear")
plt.axis("off")
plt.title(df.titles[movie_index], size=10)
plt.show()