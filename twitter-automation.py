#importing dependencies
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
from selenium.webdriver.support.ui import WebDriverWait
import itertools
from bs4 import BeautifulSoup
import requests
import googleapiclient
from googleapiclient import discovery
from googleapiclient import errors
from getpass import getpass
from time import sleep
import pandas as pd
#defining functions
def get_all_tweets_data(x):
    driver = Chrome()
    driver.get("https://www.twitter.com/login")
    wait = WebDriverWait(driver, 10)
    # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))).send_keys("mark85ha08@gmail.com")
    # wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))).send_keys("@HeroAgraw5073")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]"))).click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="password"]'))).send_keys("@Sahha08")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Log in')]"))).click()

    #x = str(input("enter the user id(without @): "))
    driver.get("https://www.twitter.com/" + x)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))).send_keys("@HeroAgraw5073")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]"))).click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="password"]'))).send_keys("@Sahha08")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Log in')]"))).click()
    sleep(5)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Posts"))).click()
    data = []
    tweet_ids = set()
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    while scrolling:
        page_cards = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
        for card in page_cards[-15:]:
            tweet = get_tweet_data(card)
            if tweet:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)

        scroll_attempt = 0
        while True:
            # check scroll position
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    sleep(2) # attempt another scroll
            else:
                last_position = curr_position
                break 
    df = pd.DataFrame(data, columns = ["date and time", "text", "reply_count", "retweet_count", "like_count"])
    return df
def get_tweet_data(card):
    """Extract data from tweet card"""
    try:
        postdate = card.find_element(By.XPATH,'.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    
    comment = card.find_element(By.XPATH,'.//div[2]/div[2]/div[1]').text
    responding = card.find_element(By.XPATH,'.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_cnt = card.find_element(By.XPATH,'.//div[@data-testid="reply"]').text
    retweet_cnt = card.find_element(By.XPATH,'.//div[@data-testid="retweet"]').text
    like_cnt = card.find_element(By.XPATH,'.//div[@data-testid="like"]').text
    tweet = (postdate, text, reply_cnt, retweet_cnt, like_cnt)
    return tweet