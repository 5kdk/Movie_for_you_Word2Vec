"""
리뷰가 유사한 영화를 찾아서 추천해주는 시스템 만들기 - crawling작업
"""

"""
crawling은 각자 진행 후 빨리 완성되는 코드로 연도를 나눠 진행
일단 2019년 개봉작만 크롤링, 나머지는 연도별로 각자 크롤링 해 합치기
저장 형식은 csv, 컬럼 명은 ['years', 'titles', 'reviews']로 통일
파일명은 reviews_0000.csv 로 설정, 앞 4자는 연도
크롤링 파일은 공유드라이버에 올리기
"""

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException  #엘리먼트가 없을 땐 무시하기
import time

#크롬드라이버 옵션 설정
options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('disable_gpu')
options.add_argument('lang=ko_KR')

driver = webdriver.Chrome('chromedriver', options=options)
titles = []
reviews = []

try:
    for i in range(1, 44):  #2019년 개봉영화 페이지 개수
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open=2019&page={}'.format(i)
        #y = driver.find_elements_by_xpath('//*[@id="old_content"]/ul/li')  #20개 영화의 엘리먼트를 가져온다,해당되는 것들을 모두 가져와야해서 elements를 사용
        # 영화 상세 페이지에 들어가는 for문
        for j in range(1, 21):  #영화 개수만큼 for문을 돌린다  (len(y)+1)
            try:
                driver.get(url)
                time.sleep(1)
                movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
                title = driver.find_element_by_xpath(movie_title_xpath).text
                print(title)
                driver.find_element_by_xpath(movie_title_xpath).click() #format함수를 사용시 %를 사용해도 되고 앞에 f를 붙여도 된다, click=사용 시 해당 엘리먼트가 클릭됨
                time.sleep(1)  #클릭해서 해당 영화페이지에 들어갈 때 시간이 소요되서 페이지가 다운되는 걸 막기 위해
                try:
                    btn_review_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
                    # 리뷰 엘리먼트를 찾은 후 클릭
                    driver.find_element_by_xpath(btn_review_xpath).click()  # 리뷰버튼 제목
                    time.sleep(1)
                    review_len_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'  #리뷰의 총 개수가 적힌 엘리먼트
                    review_len = driver.find_element_by_xpath(review_len_xpath).text  #개수를 문자로 긁어오기

                    review_len = int(review_len)  #정수값으로 바꿔서 이 값만큼 for문 돌리기
                    try:
                        for k in range(1, ((review_len -1) // 10)+2):  #(review_len // 10)=10으로 나눈 몫을 구하기 위해 (1, ((review_len -1) // 10)+2)
                            review_page_xpath = '//*[@id="pagerTagAnchor{}"]'.format(k)  #리뷰의 페이지 버튼 엘리먼트찾기
                            driver.find_element_by_xpath(review_page_xpath).click()  #리뷰 페이지버튼 클릭
                            time.sleep(1)
                            for l in range(1, 11):  #리뷰페이지 당 리뷰가 10개씩 고정
                                review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]'.format(l)  #리뷰의 제목을 클릭
                                try:
                                    driver.find_element_by_xpath(review_title_xpath).click()
                                    time.sleep(1)
                                    try:
                                        review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'  #리뷰의 내용을 가져오
                                        review = driver.find_element_by_xpath(review_xpath).text
                                        titles.append(title)
                                        reviews.append(review)
                                        driver.back()
                                        time.sleep(1)
                                    except:
                                        driver.back()
                                        time.sleep(1)
                                        print('review crawling error')
                                except:
                                    time.sleep(1)
                                    print('review title error')
                    except:
                        print('review page btn click error')
                except:
                    print('review btn click error')

            except NoSuchElementException:   #엘리먼트를 찾지 못했을 때 NoSuchElementException를 출력해준다
                driver.get(url)
                time.sleep(1)
                print('NoSuchElementException')
        print(len(reviews))
    df_review = pd.DataFrame({'titles':titles, 'reviews':reviews})
    df_review['years'] = 2019
    print(df_review.head(20))
    df_review.to_csv('./reviews_2019.csv')

except:
    print('except1')
finally:
    driver.close()


