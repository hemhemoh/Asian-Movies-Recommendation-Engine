#!/usr/bin/env python
# coding: utf-8

# # SETUP

# ### Importing the neccessary libraries

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib
from urllib.request import urlretrieve as r
import os
import requests
from lxml import html
import pandas as pd
import numpy as np
import binascii as ba
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException 
from selenium.common.exceptions import StaleElementReferenceException, JavascriptException                     
from requests import Request
from urllib.request import urlopen
from selenium.webdriver.common.by import By
from selenium.webdriver .common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[ ]:


c_path = 'C:/Users/Mardiyyah/Desktop/chromedriver_win32/chromedriver.exe'


# In[ ]:


driver = webdriver.Chrome(executable_path=c_path)
driver.maximize_window()


# In[ ]:


driver.get("https://fixdrama.com/")


# ### Scraping for korean movies

# In[ ]:


link = driver.find_element(By.LINK_TEXT, "KOREAN")
link.click()
#navigating to korean dramas


# In[ ]:


actions = ActionChains(driver)


# In[ ]:


page = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div[2]/div[2]/ul/li[7]/a').text
#finding the number of pages the korean dramas appear on
page


# In[ ]:


ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,JavascriptException)


# In[ ]:


data = []
pages = 77
while pages < int(page):
#while pages < 5:
    try:
        driver.refresh()
        module = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CLASS_NAME, "block-items")))
        titles_count = len(module.find_elements(By.XPATH, '//div[contains(@class, "col-xlg-2")]'))
        for title_idx in range(titles_count):
            tit = driver.find_element(By.XPATH, f'//div[contains(@class, "col-xlg-2")][{title_idx+1}]')
            actions.move_to_element(tit).click().perform()
            title = driver.find_element_by_xpath('//h1[@class = "movie-title text-nowrap"]').text
            rating = driver.find_element(By.XPATH, '//div[@class = "caption"]').text
            genre = driver.find_element(By.XPATH, '//h2[@class = "movie-subtitle"]').text
            summary = driver.find_element(By.TAG_NAME, 'p').text
            #year = driver.find_element(By.XPATH, '//li[@class ="common-list"]').text
            try:
                driver.execute_script("document.getElementById('mCSB_1').scrollIntoView();")
                casts = set()
                cast = driver.find_elements(By.CLASS_NAME, 'actor-info')
                for cat in cast:
                    casts.add(cat.text)
                try:
                    slider = driver.find_element(By.CLASS_NAME, 'mCSB_dragger')
                    actions.drag_and_drop_by_offset(slider, 0, 200).perform()
                    crew = driver.find_elements(By.CLASS_NAME, 'actor-info')
                    for cre in crew:
                        casts.add(cre.text)
                except ignored_exceptions:
                    pass
            except ignored_exceptions:
                casts = "not available"
            data.append({"Title": title, "Rating": rating, "Genre": genre, "Description": summary, "Casts":casts, 'Country':'Korean'})
            driver.back()
            pages += 1
            if pages <int(page):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Next »")))
                actions.move_to_element(link).click().perform()
    finally:
        print(f"{len(data)} done")

        


# In[ ]:


#converting the dictionary to a dataframe
movies_csv = pd.DataFrame.from_dict(data)


# In[ ]:


#saving the dataframe as a csv file
movies_csv.to_csv("KoreanMovies.csv", index=False)


# ### Scraping for chinese movies

# In[ ]:


#Navigating to chinese movies on the website
link = driver.find_element(By.LINK_TEXT, "CHINESE")
link.click()


# In[ ]:


page = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div[2]/div[2]/ul/li[7]/a').text
#finding the number of pages the chinese dramas appear on
page


# In[ ]:


dataC = []
pages = 0
while pages < int(page):
    try:
        driver.refresh()
        module = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CLASS_NAME, "block-items")))
        titles_count = len(module.find_elements(By.XPATH, '//div[contains(@class, "col-xlg-2")]'))
        for title_idx in range(titles_count):
            tit = driver.find_element(By.XPATH, f'//div[contains(@class, "col-xlg-2")][{title_idx+1}]')
            actions.move_to_element(tit).click().perform()
            title = driver.find_element_by_xpath('//h1[@class = "movie-title text-nowrap"]').text
            rating = driver.find_element(By.XPATH, '//div[@class = "caption"]').text
            genre = driver.find_element(By.XPATH, '//h2[@class = "movie-subtitle"]').text
            summary = driver.find_element(By.TAG_NAME, 'p').text
            try:
                driver.execute_script("document.getElementById('mCSB_1').scrollIntoView();")
                casts = set()
                cast = driver.find_elements(By.CLASS_NAME, 'actor-info')
                for cat in cast:
                    casts.add(cat.text)
                try:
                    slider = driver.find_element(By.CLASS_NAME, 'mCSB_dragger')
                    actions.drag_and_drop_by_offset(slider, 0, 200).perform()
                    crew = driver.find_elements(By.CLASS_NAME, 'actor-info')
                    for cre in crew:
                        casts.add(cre.text)
                except ignored_exceptions:
                    pass
            except ignored_exceptions: 
                casts = "not available"
            dataC.append({"Title": title, "Rating": rating, "Genre": genre, "Description": summary, "Casts":casts, 'Country':'Chinese'})
            driver.back()
        pages += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if pages < int(page):
            link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Next »")))
            actions.move_to_element(link).click().perform()
    except ignored_exceptions:
        pass
    finally:
        print(f"{len(dataC)} done")


# In[ ]:


#converting the dictionary to a dataframe
movies = pd.DataFrame.from_dict(data)


# In[ ]:


#saving the dataframe as a csv file
movies.to_csv("ChineseMovies.csv", index=False)


# ### Scraping for HongKong movies

# In[ ]:


#Navigating to hong kong movies on the website
link = driver.find_element(By.LINK_TEXT, "HK DRAMA")
link.click()


# In[ ]:


page = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div[2]/div[2]/ul/li[6]/a').text
#finding the number of pages the hongkong dramas appear on
page


# In[ ]:


dataH = []
pages = 0
while pages < int(page):
    try:
        driver.refresh()
        module = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CLASS_NAME, "block-items")))
        titles_count = len(module.find_elements(By.XPATH, '//div[contains(@class, "col-xlg-2")]'))
        for title_idx in range(titles_count):
            tit = driver.find_element(By.XPATH, f'//div[contains(@class, "col-xlg-2")][{title_idx+1}]')
            actions.move_to_element(tit).click().perform()
            title = driver.find_element_by_xpath('//h1[@class = "movie-title text-nowrap"]').text
            rating = driver.find_element(By.XPATH, '//div[@class = "caption"]').text
            genre = driver.find_element(By.XPATH, '//h2[@class = "movie-subtitle"]').text
            summary = driver.find_element(By.TAG_NAME, 'p').text
            try:
                driver.execute_script("document.getElementById('mCSB_1').scrollIntoView();")
                casts = set()
                cast = driver.find_elements(By.CLASS_NAME, 'actor-info')
                for cat in cast:
                    casts.add(cat.text)
                try:
                    slider = driver.find_element(By.CLASS_NAME, 'mCSB_dragger')
                    actions.drag_and_drop_by_offset(slider, 0, 200).perform()
                    crew = driver.find_elements(By.CLASS_NAME, 'actor-info')
                    for cre in crew:
                        casts.add(cre.text)
                except ignored_exceptions:
                    pass
            except ignored_exceptions: 
                casts = "not available"
            dataH.append({"Title": title, "Rating": rating, "Genre": genre, "Description": summary, "Casts":casts, 'Country':'HongKong'})
            driver.back()
        pages += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if pages < int(page):
            link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Next »")))
            actions.move_to_element(link).click().perform()
    except ignored_exceptions:
        pass
    finally:
        print(f"{len(dataH)} done")


# In[ ]:


#converting the dictionary to a dataframe
hk_movies = pd.DataFrame.from_dict(data)


# In[ ]:


#saving the dataframe as a csv file
hk_movies.to_csv("HongKongMovies.csv", index=False)


# ### Scraping for Thailand Movies 

# In[ ]:


#Navigating to thailand movies on the website
link = driver.find_element(By.LINK_TEXT, "THAILAND")
link.click()


# In[ ]:


page = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div[2]/div[2]/ul/li[7]/a').text
#finding the number of pages the thailand dramas appear on
page


# In[ ]:


dataT = []
pages = 0
while pages < int(page):
    try:
        driver.refresh()
        module = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CLASS_NAME, "block-items")))
        titles_count = len(module.find_elements(By.XPATH, '//div[contains(@class, "col-xlg-2")]'))
        for title_idx in range(titles_count):
            tit = driver.find_element(By.XPATH, f'//div[contains(@class, "col-xlg-2")][{title_idx+1}]')
            actions.move_to_element(tit).click().perform()
            title = driver.find_element_by_xpath('//h1[@class = "movie-title text-nowrap"]').text
            rating = driver.find_element(By.XPATH, '//div[@class = "caption"]').text
            genre = driver.find_element(By.XPATH, '//h2[@class = "movie-subtitle"]').text
            summary = driver.find_element(By.TAG_NAME, 'p').text
            #year = driver.find_element(By.XPATH, '//li[@class ="common-list"]').text
            try:
                driver.execute_script("document.getElementById('mCSB_1').scrollIntoView();")
                casts = set()
                cast = driver.find_elements(By.CLASS_NAME, 'actor-info')
                for cat in cast:
                    casts.add(cat.text)
                try:
                    slider = driver.find_element(By.CLASS_NAME, 'mCSB_dragger')
                    actions.drag_and_drop_by_offset(slider, 0, 200).perform()
                    crew = driver.find_elements(By.CLASS_NAME, 'actor-info')
                    for cre in crew:
                        casts.add(cre.text)
                except ignored_exceptions:
                    pass
            except ignored_exceptions:
                casts = "not available"
            dataT.append({"Title": title, "Rating": rating, "Genre": genre, "Description": summary, "Casts":casts, 'Country':'Thailand'})
            driver.back()
        pages += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if pages < int(page):
            link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Next »")))
            actions.move_to_element(link).click().perform()
    except ignored_exceptions:
        pass
    finally:
        print(f"{len(dataT)} done")


# In[ ]:


#converting the dictionary to a dataframe
thai_movies = pd.DataFrame.from_dict(dataT)


# In[ ]:


#saving the dataframe as a csv file
thai_movies.to_csv("ThaiLandMovies.csv", index= False)

