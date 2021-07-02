import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
import matplotlib as mpl

# 워드 클라우드 폰트 path
cloudfontpath = '../font/Jalnan.ttf'

# plt 한글 출력
font_path = "C:/Windows/Fonts/Malgun.TTF"
font = font_manager.FontProperties(fname=font_path).get_name() 
rc('font', family=font)

embedding_model = Word2Vec.load('../models/word2VecModel_2015_2021.model')
key_word = '전율'
sim_word = embedding_model.wv.most_similar(key_word, topn=10)
print(sim_word)

vectors = []
labels = []
for label, _ in sim_word:
    labels.append(label)
    vectors.append(embedding_model.wv.get_vector(label))
df_vectors = pd.DataFrame(vectors)
print(df_vectors.head())

tsne_model = TSNE(perplexity=40, n_components=2,
                  init='pca', n_iter=2500, random_state=23)
new_values = tsne_model.fit_transform(df_vectors)
df_xy = pd.DataFrame({'words':labels,
                      'x':new_values[:, 0],
                      'y':new_values[:, 1]})
print(df_xy.head())

print(df_xy.shape)
df_xy.loc[df_xy.shape[0]] = (key_word, 0, 0)
plt.figure(figsize=(8, 8))
plt.scatter(0, 0, s=700, c='darkorange', marker='*')
for i in range(len(df_xy.x)):
    a = df_xy.loc[[i, 10], :]
    plt.plot(a.x, a.y, c='royalblue', linestyle='--', marker='D', linewidth=1)
    plt.annotate(df_xy.words[i], xytext=(5, 2),
                 xy=(df_xy.x[i], df_xy.y[i]),
                 textcoords='offset points',
                 ha='right', va='bottom')
plt.show()
