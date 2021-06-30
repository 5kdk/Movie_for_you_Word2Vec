"""
리뷰가 유사한 영화를 찾아서 추천해주는 시스템 만들기 - crawling작업
네이버 영화 사이트
"""

"""
crawling은 각자 진행 후 빨리 완성되는 코드로 연도를 나눠 진행
일단 2019년 개봉작만 크롤링, 나머지는 연도별로 각자 크롤링 해 합치기
저장 형식은 csv, 컬럼 명은 ['titles', 'reviews']로 통일
파일명은 reviews_0000.csv 로 설정, 앞 4자는 연도
크롤링 파일은 공유드라이버에 올리기
"""

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException  #엘리먼트가 없을 땐 무시하기

#크롬드라이버 옵션 설정
options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('disable_gpu')
options.add_argument('lang=ko_KR')

driver = webdriver.Chrome('chromedriver', options=options)
year = []
name = []
reviewcontext = []

for i in range(1, 44):
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open=2019&page={}'.format(i)
    driver.get(url)

driver.close()