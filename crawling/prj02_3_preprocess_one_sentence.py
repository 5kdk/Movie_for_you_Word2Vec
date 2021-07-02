import pandas as pd

#데이터 불러오기
df = pd.read_csv('../data/cleaned_review_2016.csv', index_col=0)
df.dropna(inplace=True)
df.to_csv('../data/cleaned_review_2016.csv')

one_sentences = []
for idx, title in enumerate(df['titles'].unique()):  #제목은 하나씩만 가져오기
    temp = df[df['titles'] == title]['cleaned_sentences']  #제목에 해당하는 리뷰들을 가져오기
    one_sentence = ' '.join(temp)  #각각의 문장을 하나로 이어준다
    one_sentences.append(one_sentence)  #리스트에 합쳐진 문장들을 넣어준다

#새로운 데이터 프레임 만들기 = 영화 하나 당 합쳐진 리뷰 하나로 넣어주기
df_one_sentences = pd.DataFrame({'titles':df['titles'].unique(), 'reviews':one_sentences})
print(df_one_sentences.head())
#파일 저장
df_one_sentences.to_csv('../data/one_sentence_review_2016.csv')