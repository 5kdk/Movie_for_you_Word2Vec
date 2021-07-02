import pandas as pd
import matplotlib.pyplot as pl
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
key_word = '소름'
sim_word = embedding_model.wv.most_similar(key_word, topn=10)
print(sim_word)