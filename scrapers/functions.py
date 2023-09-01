import os
import re
import time
import csv
import pickle
import random
import argparse
import pandas as pd
from tqdm import tqdm

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def yt_links(key, value, base_url, n_links=250): 

    # for key in label_dict:
    #     for value in label_dict[key]:

    webdriver_path = "/usr/local/bin/geckodriver"
    options = Options()
    options.set_preference('profile', webdriver_path)
    


    query_link = base_url + value
    links = []
    driver = Firefox(options=options)
    driver.get(query_link)
    driver.maximize_window() # for maxmizing the window

    while len(set(links)) < n_links:
        # print(len(set(links)))
        time.sleep(3)
        links = list(set(links))
        links.extend(link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, '.title-and-badge.style-scope.ytd-video-renderer > a'))
        # print(links)
        # print(len(links))
        
        time.sleep(1)
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.title-and-badge.style-scope.ytd-video-renderer > a')))

        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(5)

        # print(len(set(links)))
        # print(links)
    driver.close()
    
    for link in list(set(links)):
        if "shorts" in link:
            continue
        else:
            with open(f"{key}_{value}.csv", "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([link, f"{key},{value}"])

    return list(set(links))