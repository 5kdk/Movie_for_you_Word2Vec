import collections

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from konlpy.tag import Okt
from matplotlib import font_manager, rc

from wordcloud import WordCloud
import wordcloud

# wordcloud, plt에 사용할 폰트
font_wc = "./JalnanOTF.otf"
font_plt = "C:/Windows/Fonts/NanumSquareL.ttf"
# plt 한글 출력
font = font_manager.FontProperties(fname=font_plt).get_name()
rc("font", family=font)

# 데이터 로드
df = pd.read_csv("../data/one_sentence_review_2017.csv", index_col=0)
df.dropna(inplace=True)
print(df.info())
print(df.head())

# 원하는 영화 제목 선택
movie_index = df[df["titles"] == "넘버원 전화사기단 (Thank You For Calling)"].index[0]
print(df.reviews[movie_index])

# stopword
stopword = ["관객", "작품", "주인공", "개봉"]

# wordcloud 만들어 plot
wordcloud_img = WordCloud(
    background_color="white", max_words=2000, font_path=font_wc, stopwords=stopword
).generate(df.reviews[movie_index])
plt.figure(figsize=(8, 8))
plt.imshow(wordcloud_img, interpolation="bilinear")
plt.axis("off")
plt.title(df.titles[movie_index], size=12)
plt.show()
