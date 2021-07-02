"""
워드투벡을 시각화해서 나타내기
"""
#모듈 불러오기
import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
import matplotlib as mpl

#폰트 설정하기
font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False  #한글폰트 사용시 그래프에서 마이너스 폰트 깨지는 문제에 대한 대처
rc('font', family=font_name)

#워드 투벡터라이징 한 모델 불러오기
embedding_model = Word2Vec.load('./models/word2vecModel_2015_2021.model')
key_word = '소녀시대'  #지정 단어 설정
sim_word = embedding_model.wv.most_similar(key_word, topn=10)  #지정 단어에 대해 유사한 단어 10가지를 선택
print(sim_word)


vectors = []
labels = []
for label, _ in sim_word:
    labels.append(label) #단어를 for문으로 돌리기
    print(label)
    vectors.append(embedding_model.wv[label])  #돌린 단어에 대해 모델에 넣고 워드투벡을 해준다 = 100차원으로 만들어준다

df_vectors = pd.DataFrame(vectors)
print(df_vectors.head())

#2차원 공간에 투시를 했을 때 나오는 모습
tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
new_values = tsne_model.fit_transform(df_vectors)
df_xy = pd.DataFrame({'words':labels, 'x':new_values[:, 0], 'y':new_values[:, 1]})  #컬럼을 라벨, x축, y축으로 데이터프레임 만들기
print(df_xy.head())
print(df_xy.shape)

#plt로 나타내기
df_xy.loc[df_xy.shape[0]] = (key_word, 0, 0)  #라벨을 (0, 0)점으로 잡아주기
plt.figure(figsize=(8, 8))  #이미지 크기
plt.scatter(0, 0, s=1500, marker='*')  #* 문장으로 마커를 찍어준다, 1500= 마커사이즈
for i in range(len(df_xy.x)):
    a = df_xy.loc[[i, 10], :]
    plt.plot(a.x, a.y, '-D', linewidth=2)
    #annotate = plt의 주석을 다는 것, df_xy.words[i]=좌표의 이름, xytext=주석을 표시할 xy좌표를 설정할 때 사용,xy=화살표가 가르키는 점의 위치, 'offset points=xy(좌표 측의 값)에서부터 xytext offset 위치(단위 point)에 출력

    plt.annotate(df_xy.words[i], xytext=(5, 2), xy=(df_xy.x[i], df_xy.y[i]), textcoords='offset points', ha='right', #xy=화살표가 가르키는 점의 위치, ha=horizontal alignment, va=vetical alignment
                 va='bottom')

plt.show()


