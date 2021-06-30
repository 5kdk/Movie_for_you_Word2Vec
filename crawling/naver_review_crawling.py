"""
<<<<<<< HEAD
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
from selenium.common.exceptions import NoSuchElementException  # 엘리먼트가 없을 땐 무시하기
import time

# 크롬드라이버 옵션 설정
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument("disable_gpu")
options.add_argument("lang=ko_KR")

driver = webdriver.Chrome("chromedriver", options=options)
years = []
titles = []
reviews = []

"""
영화별 xpath
1 - //*[@id="old_content"]/ul/li[1]/a
2 - //*[@id="old_content"]/ul/li[2]/a


#for 문 돌리기 전 테스트용
url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open=2019&page=1'
driver.get(url)
y = driver.find_elements_by_xpath('//*[@id="old_content"]/ul/li')
driver.find_element_by_xpath('//*[@id="old_content"]/ul/li[1]/a').click() #format함수를 사용시 %를 사용해도 되고 앞에 f를 붙여도 된다, click=사용 시 해당 엘리먼트가 클릭됨
time.sleep(0.5)  #클릭해서 해당 영화페이지에 들어갈 때 시간이 소요되서 페이지가 다운되는 걸 막기 위해
driver.find_element_by_xpath('//*[@id="movieEndTabMenu"]/li[6]/a/em').click()
print(len(y))
"""

for i in range(1, 3):  # 2019년 개봉영화 페이지 개수
    url = "https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open=2019&page={}".format(i)
    # 영화 상세 페이지에 들어가는 for문
    for j in range(1, 3):  # 영화 개수만큼 for문을 돌린다  (len(y)+1)
        try:
            driver.get(url)
            time.sleep(0.7)
            driver.find_element_by_xpath(
                '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
            ).click()  # format함수를 사용시 %를 사용해도 되고 앞에 f를 붙여도 된다, click=사용 시 해당 엘리먼트가 클릭됨
            time.sleep(0.7)  # 클릭해서 해당 영화페이지에 들어갈 때 시간이 소요되서 페이지가 다운되는 걸 막기 위해
            # 리뷰 엘리먼트를 찾은 후 클릭
            driver.find_element_by_xpath('//*[@id="movieEndTabMenu"]/li[6]/a/em').click()
            time.sleep(0.7)
            # 리뷰 전체 엘리먼트를 찾는다
            x = driver.find_elements_by_xpath('//*[@id="reviewTab"]/div/div/ul/li')
            if x:
                for k in range(1, 3):  # 각각의 x에 대한 for문, 리뷰를 하나씩 가져오기  (1, len(x)+1)
                    try:
                        # 리뷰의 제목을 클릭
                        driver.find_element_by_xpath(
                            '//*[@id="reviewTab"]/div/div/ul/li[{}]'.format(k)
                        ).click()
                        time.sleep(0.7)
                        name = driver.find_element_by_xpath(
                            '//*[@id="content"]/div[1]/div[2]/div[1]/h3/a'
                        ).text  # 영화 제목을 가져온다
                        reviewcontext = driver.find_element_by_xpath(
                            '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'
                        ).text  # 영화 리뷰 전체를 가져온다
                        # 읽어 온 내용을 빈 리스트에 추가해준다
                        titles.append(name)
                        reviews.append(reviewcontext)
                        driver.back()  # 리뷰를 하나 가져오면 다시 전 페이지로 돌아가 다음 리뷰를 선택하기 위해 back
                    except:
                        print("NoSuchElementException")

        except NoSuchElementException:  # 엘리먼트를 찾지 못했을 때 NoSuchElementException를 출력해준다
            driver.get(url)
            print("NoSuchElementException")

driver.close()

# 크롤링한 데이터를 데이터프레임으로 만들기
df = pd.DataFrame(columns=["years", "titles", "reviews"])
df["years"] = 2019
df["titles"] = titles
df["reviews"] = reviews

print(df.head(20))
=======
crawling code using multiprocessing
columms=['titles', 'reviews']
DataFrame으로 작업 후 csv로 저장
filename: reviews_YYYY.csv
"""
import requests
import re
import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from multiprocessing import Pool
from selenium.common.exceptions import NoSuchElementException


def crawler(year, list_start, list_step, review_start, review_step):
    for page in range(list_start, list_start + list_step):
        BASE_URL = "https://movie.naver.com/movie/bi/mi/point.nhn?"
        url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open={year}&page={page}"
        chromedriver = "./chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("disable_gpu")
        options.add_argument("lang=ko_KR")

        response = requests.get(url)
        df_reviews = pd.DataFrame()
        if response.ok:
            soup = bs(response.text, "html.parser")

            anchors = soup.select(".directory_list > li > a")
            re_code = re.compile("code=[0-9]*")
            hrefs = [
                (re_code.search(anchor.attrs["href"]).group(), anchor.text) for anchor in anchors
            ]

            driver = webdriver.Chrome(chromedriver, options=options)
            driver.implicitly_wait(10)

            for href, title in hrefs:
                for page_review in range(review_start, review_start + review_step):
                    try:
                        BASE_URL = f"https://movie.naver.com/movie/bi/mi/review.nhn?{href}&page={page_review}"
                        driver.get(BASE_URL)
                        if driver.find_element_by_xpath('//span[@class="cnt"]/em').text == "0":
                            break
                        page_current = driver.find_element_by_xpath(
                            '//div[@class="paging"]//span[@class="on"]'
                        ).text
                        if int(page_current) == page_review:
                            review_pages = driver.find_elements_by_xpath(
                                '//ul[@class="rvw_list_area"]/li/a'
                            )
                            reviews = []
                            for i in range(1, len(review_pages) + 1):
                                try:
                                    driver.find_element_by_xpath(
                                        f'//ul[@class="rvw_list_area"]/li[{i}]/a'
                                    ).click()
                                    review = driver.find_element_by_xpath(
                                        '//*[@class="user_tx_area"]'
                                    ).text
                                    driver.back()
                                    reviews.append(review)
                                except Exception as e:
                                    print(e)
                            df = pd.DataFrame(reviews, columns=["reviews"])
                            df["titles"] = title
                            df["years"] = year
                            df_reviews = pd.concat([df_reviews, df], ignore_index=True)
                        else:
                            break
                    except NoSuchElementException:
                        print("NoSuchElementException")
            driver.close()
    return df_reviews


if __name__ == "__main__":
    processes = 6  # 코어 수
    total_list = 6  # 연도별 크롤링할 페이지 수 / 총 영화 수는 대략 total_list * 10
    list_step = round(total_list / processes)
    review_step = 1  # 리뷰 크롤링할 페이지 수 / 총 리뷰 수는 대략 review_step * 10?
    iterable = [[2019, i * list_step + 1, list_step, 1, review_step] for i in range(processes)]
    print(iterable)
    pool = Pool(processes=processes)
    results = pool.starmap(crawler, iterable)
    pool.close()
    pool.join()
    df_concat = pd.concat(results, ignore_index=True)
    df_concat.to_csv("../crawling_data/reviews_2019.csv", index=False)
    print(df_concat)
>>>>>>> upstream/main
