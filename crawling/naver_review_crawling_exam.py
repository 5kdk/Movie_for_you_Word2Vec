from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchAttributeException, NoSuchElementException
import time

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('disable_gpu')
options.add_argument('lang=ko_KR')

driver = webdriver.Chrome('./chromedriver.exe', options=options)
years = []
titles = []
reviews = []
try:
    for i in range(0, 44): # 2019년 개봉영화
        url = f'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open=2019&page={i}'
        time.sleep(0.5)
        #y = driver.find_elements_by_xpath('//*[@id="old_content"]/ul/li')
        #for j in range(1, len(y)+1): # 영화 갯수 상세
        for j in range(1, 3):
            try:
                driver.get(url)
                time.sleep(1)
                movie_title_xpath = f'//*[@id="old_content"]/ul/li[{j}]/a'
                title = driver.find_element_by_xpath(movie_title_xpath).text
                print(title)
                driver.find_element_by_xpath(movie_title_xpath).click() # 제목 버튼 클릭
                time.sleep(1)
                try:
                    btn_review_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a/em'
                    driver.find_element_by_xpath(btn_review_xpath).click()  # 리뷰버튼 제목
                    time.sleep(1)
                    review_len_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
                    review_len = driver.find_element_by_xpath(review_len_xpath).text
                    
                    review_len = int(review_len)
                                       
                    try:
                        #for k in range(1, ((review_len-1) // 10) + 2):    
                        for k in range(1, 2):
                            review_page_xpath = f'//*[@id="pagerTagAnchor{k}]/span'
                            driver.find_element_by_xpath(review_page_xpath).click()
                            time.sleep(1)
                            #for l in range(1, 11):
                            for l in range(1, 2):
                                review_title_xpath = f'//*[@id="reviewTab"]/div/div/ul/li[{k}]'
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

            except NoSuchElementException:
                driver.get(url)
                time.sleep(1)
                print('NoSuchElementException')
        print(len(reviews))
    df_review = pd.DataFrame({'titles':titles, 'reviews':reviews})
    df_review['years'] = 2019
    print(df_review.head(20))
    df_review.to_csv('./crawling_data/reviews_2019_exam.csv')

except:
    print('except1')
finally:
    driver.close()