import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from konlpy.tag import Okt
import matplotlib as mpl
from matplotlib import font_manager, rc

# import matplotlib as mpl
# import matplotlib.font_manager as fm
# fontpath = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
# font = fm.FontProperties(fname=fontpath, size=9)
# plt.rc('font', family='NanumBarunGothic')
# mpl.font_manager._rebuild()

fontpath = './malgun.ttf'
font_name = font_manager.FontProperties(fname=fontpath).get_name()
rc('font', family=font_name)
mpl.font_manager._rebuild()
df = pd.read_csv('../crawling_data/one_sentence_review_2020.csv', index_col=0)
df.dropna(inplace=True)
#print(df.info())

print(df.head(20))

movie_index = df[df['titles'] == '다만 악에서 구하소서 (DELIVER US FROM EVIL)'].index[0]
#print(movie_index)
print(df.reviews[movie_index])
words = df.reviews[movie_index].split(' ')
print(words)

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)
stopwords = ['관객', '작품', '주인공', '개봉', '촬영']
wordcloud_img = WordCloud(
    background_color='white', max_words=2000,
    font_path=fontpath,
    stopwords=stopwords
    ).generate(df.reviews[movie_index])
# wordcloud_img = WordCloud(
#     background_color='white', max_words=2000,
#     font_path=fontpath
#     ).generate_from_frequencies(worddict)
plt.figure(figsize=(8,8))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.title(df.titles[movie_index], size=25)
plt.show()