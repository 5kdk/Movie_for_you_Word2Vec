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
key_word = '엄마'  #지정 단어 설정
sim_word = embedding_model.wv.most_similar(key_word, topn=10)  #지정 단어에 대해 유사한 단어 10가지를 선택
print(sim_word)