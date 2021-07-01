"""
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


def crawler(year, list_start, list_end, review_start, review_step):
    chromedriver = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    # options.add_argument("--headless")
    options.add_argument("disable_gpu")
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(chromedriver, options=options)
    driver.implicitly_wait(10)
    
    df_reviews = pd.DataFrame()
    for page in range(list_start, list_end + 1):
        url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open={year}&page={page}"

        response = requests.get(url)
        if response.ok:
            soup = bs(response.text, "html.parser")

            anchors = soup.select(".directory_list > li > a")
            re_code = re.compile("code=[0-9]*")
            hrefs = [
                (re_code.search(anchor.attrs["href"]).group(), anchor.text) for anchor in anchors
            ]


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
    processes = 14  # 코어 수
    total_list = 71  # 연도별 크롤링할 페이지 수 / 총 영화 수는 대략 total_list * 10
    list_step = np.linspace(1, total_list + 1, processes + 1, dtype=int) 
    review_step = 10  # 리뷰 크롤링할 페이지 수 / 총 리뷰 수는 대략 review_step * 10?
    year = 2015
    iterable = [[year, list_step[i], list_step[i + 1] - 1, 1, review_step] for i in range(processes)]
    print(iterable)
    pool = Pool(processes=processes)
    results = pool.starmap(crawler, iterable)
    pool.close()
    pool.join()
    df_concat = pd.concat(results, ignore_index=True)
    df_concat.to_csv(f"../crawling_data/reviews_{year}.csv", index=False)
    print(df_concat)
    