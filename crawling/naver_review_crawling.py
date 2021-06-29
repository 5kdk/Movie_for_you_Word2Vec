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
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from multiprocessing import Pool
from selenium.common.exceptions import NoSuchElementException


def crawler(year, list_start, list_step, review_start, review_step):
    for page in range(list_start, list_start + list_step):
        BASE_URL = "https://movie.naver.com/movie/bi/mi/point.nhn?"
        url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open={year}&page={page}"
        chromedriver = "./chromedriver.exe"

        response = requests.get(url)
        df_reviews = pd.DataFrame()
        if response.ok:
            soup = bs(response.text, "html.parser")

            anchors = soup.select(".directory_list > li > a")
            re_code = re.compile("code=[0-9]*")
            hrefs = [
                (re_code.search(anchor.attrs["href"]).group(), anchor.text) for anchor in anchors
            ]

            driver = webdriver.Chrome(chromedriver)
            driver.implicitly_wait(3)

            for href, title in hrefs:
                for page_review in range(review_start, review_start + review_step):
                    try:
                        BASE_URL = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?{href}&page={page_review}"
                        driver.get(BASE_URL)
                        if driver.find_element_by_xpath('//strong[@class="total"]/em').text == "0":
                            break
                        page_current = driver.find_element_by_xpath(
                            '//div[@class="paging"]//span[@class="on"]'
                        ).text
                        if int(page_current) == page_review:
                            reviews = driver.find_elements_by_xpath('//div[@class="score_reple"]/p')
                            reviews = [review.text for review in reviews]
                            df = pd.DataFrame(reviews, columns=["reviews"])
                            df["titles"] = title
                            df_reviews = pd.concat([df_reviews, df], ignore_index=True)
                        else:
                            break
                    except NoSuchElementException:
                        print("NoSuchElementException")
            driver.close()
    return df_reviews


if __name__ == "__main__":
    processes = 6
    total_list = 6
    list_step = round(total_list / processes)
    review_step = 1
    iterable = [[2019, i * list_step + 1, list_step, 1, review_step] for i in range(processes)]
    print(iterable)
    pool = Pool(processes=processes)
    results = pool.starmap(crawler, iterable)
    pool.close()
    pool.join()
    df_concat = pd.concat(results, ignore_index=True)
    df_concat.to_csv("../crawling_data/reviews_2019.csv", index=False)
    print(df_concat)
