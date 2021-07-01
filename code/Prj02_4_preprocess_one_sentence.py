import pandas as pd

years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]

for year in years:
    
    #데이터 불러오기
    df = pd.read_csv(f'../crawling_data/cleaned_review_{year}.csv',
                    index_col=0)
    df.dropna(inplace=True)

    one_sentences = []
    for idx, title in enumerate(df['titles'].unique()):  # 고유 title 추출
        temp = df[df['titles'] == title]['cleaned_sentences']  
        one_sentence = ' '.join(temp) 
        one_sentences.append(one_sentence)

    # 새로운 데이터 프레임
    df_one_sentences = pd.DataFrame({'titles':df['titles'].unique(), 'reviews':one_sentences})
    print(df_one_sentences.head())
    # 파일 저장
    df_one_sentences.to_csv(f'../crawling_data/one_sentence_review_{year}.csv')
