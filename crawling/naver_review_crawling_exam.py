#crawling 작업

#crawling은 각자 진행하고 빨리 왼성되는 코드로 연도를 나눠서 진행하겠습니다.
#일단 2019년 개봉작만 크롤링 해주시고 나머지는 연도별로 크롤링해서 합칠게요.
#데이터는 데이터프레임으로 작업해주시고 저장 형식은 csv로 하겠습니다.
#컬럼 명은 ['years','titles', 'reviews']로 통일해 주세요.
#파일명은 reviews_0000.csv 로 해주세요. 0000은 연도입니다.
#크롤링 파일은 https://url.kr/74bjw5 요기에 올려주세요.

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('disable_gpu')
options.add_argument('lang=ko_KR')

driver = webdriver.Chrome('chromedriver', options=options)
titles = []
reviews = []
try:
    for i in range(1,44): # 연도별 영화 리스트 페이지수 확인하세요
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open=2019&page={}'.format(i)

        for j in range(1,21): #영화 제목 리스트 페이지당 20개
            try:
                driver.get(url)
                time.sleep(1)
                movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
                title = driver.find_element_by_xpath(movie_title_xpath).text
                print(title)
                driver.find_element_by_xpath(movie_title_xpath).click()
                time.sleep(1)
                try:
                    btn_review_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a/em'
                    driver.find_element_by_xpath(btn_review_xpath).click()  # 리뷰버튼 제목
                    time.sleep(1)
                    review_len_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
                    review_len = driver.find_element_by_xpath(review_len_xpath).text

                    review_len = int(review_len.replace(',',''))
                    if review_len > 50:
                        review_len = 50
                    try:
                        for k in range(1, ((review_len-1) // 10)+2):
                            review_page_xpath = '//*[@id="pagerTagAnchor{}"]/span'.format(k)
                            driver.find_element_by_xpath(review_page_xpath).click()
                            time.sleep(1)
                            for l in range(1,11):
                                review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]'.format(l)
                                try:
                                    driver.find_element_by_xpath(review_title_xpath).click()
                                    time.sleep(1)
                                    try:
                                        review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'
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
                                    print('review title click error')

                    except:
                        print('review page btn click error')
                except:
                    print('review btn click error')
                df_review = pd.DataFrame({'titles': titles, 'reviews': reviews})
                df_review.to_csv('./reviews_2019_{}.csv'.format(j + (i - 1) * 20))
            except NoSuchElementException:
                driver.get(url)
                time.sleep(1)
                print('NoSuchElementException')
        print(len(reviews))
        df_review = pd.DataFrame({'titles': titles, 'reviews': reviews})
        print(df_review.head(20))
        df_review.to_csv('./reviews_2019_{}_page.csv'.format(i))
    df_review = pd.DataFrame({'titles': titles, 'reviews': reviews})
    df_review.to_csv('./reviews_2019_.csv')
except:
    print('except1')
finally:
    driver.close()