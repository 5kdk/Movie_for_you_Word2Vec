"""
크롤링과 전처리한 데이터를 중복 제거하고 합치기
"""

import pandas as pd

#중복된 데이터 제거 코드
# df_dup = pd.read_csv('./crawling_data/cleaned_review_2015.csv', index_col=0)  #데이터 불러오기
# df_undup = df_dup.drop_duplicates()  #중복 제거
# print(df_undup.duplicated().sum())  #중복제거 된 데이터에서 중복이 있는지 확인, 0이 나와야한다
# df_undup.to_csv('./crawling_data/cleaned_review_2015.csv')  #기존 파일에 덮어쓰기
# exit()

df = pd.read_csv('./crawling_data/cleaned_review_2015.csv', index_col=0)  #데이터 불러오기
print(df.info())
df.dropna(inplace=True)  #결측치 제거
df.drop_duplicates()  #중복 제거
df.columns = ['titles', 'cleaned_reviews']  #클롤링한 데이터 별로 컬럼이 다를까봐 맞춰주기
df.to_csv('./crawling_data/cleaned_review_2015.csv')

#for문으로 데이터 불러와 합치기
for i in range(16, 22):
    df_temp = pd.read_csv('./crawling_data/cleaned_review_20{}.csv'.format(i), index_col=0)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates()
    df_temp.columns = ['titles', 'cleaned_reviews']  # 클롤링한 데이터 별로 컬럼이 다를까봐 맞춰주기
    df_temp.to_csv('./crawling_data/cleaned_review_20{}.csv'.format(i))
    df = pd.concat([df, df_temp], ignore_index=True)  #기존에 15년도 데이터 프레임에 이어붙이기

print(df.info())
df.to_csv('./crawling/movie_review_2015_2021.csv')
