# function for scrapping the reviews pages.
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd


def scrape_review_page(browser):
    out = dict()
    df = pd.DataFrame()
    page_source = browser.page_source
    soup = bs(page_source, 'lxml')

    id_list = list()
    for a in soup.find_all('div', class_='a-section a-spacing-none reviews-content a-size-base'):
        for b in a.find_all('div', class_='a-section a-spacing-none reviews-content a-size-base'):
            for c in b.find_all('div', class_='a-section review aok-relative'):
                id_value = c["id"]
                id_list.append(id_value)

    for l in id_list:
        try:
            review = browser.find_element(
                By.XPATH, f'//*[@id="customer_review-{l}"]/div[4]/span/span').text
            verified_purchase = browser.find_element(
                By.XPATH, f'//*[@id="customer_review-{l}"]/div[3]/span/a/span').text
            review_title = browser.find_element(
                By.XPATH, f'//*[@id="customer_review-{l}"]/div[2]/a[2]/span').text
            review_of_text = browser.find_element(
                By.XPATH, f'//*[@id="customer_review-{l}"]/span').text
            text = browser.find_element(
                By.XPATH, f'//*[@id="customer_review-{l}"]/div[3]/a').text
            color = text.split('Size')[0].split(': ')[-1]
            style_name = text.split('name:')[1].strip(' ').split('Pattern')[0]
        except:
            pass

        out = {
            'review_title': review_title,
            'review_of_text': review_of_text,
            'color': color,
            'style_name': style_name,
            'verified_purchase': verified_purchase,
            'review': review
        }

        df = df.append(out, ignore_index=True)
        # print(f"df:{df}")
    return df


browser = webdriver.Chrome()  
url = 'https://www.amazon.in/Apple-New-iPhone-12-128GB/dp/B08L5TNJHG/' #Amazon Iphone 12 page url

browser.maximize_window()
browser.get(url)  # getting the page

browser.find_element(By.XPATH, '//*[@id="reviews-medley-footer"]/div[2]/a').click() # click for all reviews page
df_final = pd.DataFrame()
for i in range(20):    # scrapping 20 reviews page 
    df = scrape_review_page(browser)    #calling scrapping function
    df_final = df_final.append(df, ignore_index=True)  #appending the values to the Dataframe
    browser.find_element( By.XPATH, '//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').click()  # next page
    time.sleep(3)

browser.quit()   #quiting browser
df_final.to_csv('review_data.csv')   # Saving the scrapped data to csv
