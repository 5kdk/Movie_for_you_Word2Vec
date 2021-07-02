import pandas as pd
from glob import glob

#files = glob("../processing_data/cleaned_review_*.csv")
files = glob("../processing_data/one_sentence_review_*.csv")
df = pd.DataFrame()

# 중복 및 null 제거 후 concat
print(files)
for file in files:
    df_temp = pd.read_csv(file, index_col=0)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    print(df_temp.duplicated().sum())
    df = pd.concat([df, df_temp])

print(df.info())
#df.to_csv("../processing_data/movie_review_2015_2021.csv", index=False)
df.to_csv("../processing_data/movie_review_one_sentence_2015-2021.csv", index=False)