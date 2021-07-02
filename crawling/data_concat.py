import pandas as pd
from glob import glob

files_c = glob("../clean_data/cleaned_review_*.csv")
files_o = glob("../crawling_data/one_sentence_review_*.csv")
df_cleaned = pd.DataFrame()
df_one = pd.DataFrame()
# 중복 및 null 제거 후 concat
print(files_c)
print(files_o)
for file in files_c:
    df_temp = pd.read_csv(file, index_col=0)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    print(df_temp.duplicated().sum())
    df_cleaned = pd.concat([df_cleaned, df_temp])

for file in files_o:
    df_temp = pd.read_csv(file, index_col=0)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    print(df_temp.duplicated().sum())
    df_one = pd.concat([df_one, df_temp])

print(df_cleaned.info())
print(df_cleaned.head(10))
print(df_one.info())
print(df_one.head(10))

df_cleaned.to_csv("../crawling_data/movie_review_2015-2021.csv", index=False)
df_one.to_csv("../crawling_data/movie_review_one_sentence_2015-2021.csv", index=False)
