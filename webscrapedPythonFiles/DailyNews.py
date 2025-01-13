# -*- coding: utf-8 -*-

#importing libraries
import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd    
from selenium import webdriver
import time

#path where the chromedriver.exe file is saved
Path = 'C:\Program Files (x86)\chromedriver.exe'

#automatically opening the web page of the given url in google chrome 
driver = webdriver.Chrome(Path)
#obtaining news items in 'Law and Order' section of Daily News news paper
driver.get('https://dailynews.lk/category/security')

#obtaining news items in business section of Daily News news paper
#In order to obtain the business news articles make the line 16 as a comment and uncomment the 21st line 
#and run again the whole code after making the changes in lines 50 and 112 as described in comments near by
##driver.get('https://dailynews.lk/category/business')

#obtaining news items in political section Daily News news paper
#In order to obtain the political news articles make the line 16 as a comment and uncomment the 26th line 
#and run again the whole code after making the changes in lines 50 and 112 as described in comments near by
##driver.get('https://dailynews.lk/category/political')


#stopping the proramme for 5 seconds until the given page load
time.sleep(5)


#######################################################################
####To run until the end of the site.As there's no need to extract news items from the begining, this section is kept as a comment. (Just to get an idea.)
# i=1
# click_more = True
# while click_more:
#     time.sleep(10)
#     element = driver.find_element_by_class_name('pager-next')
    
#     print(i)
#     i=i+1
#     if element:
#         element.click()
#         time.sleep(10)
#     else:
#         click_more = False
########################################################################
#the value assigns to 'page_no' variable should be changed accordingly. The number of pages where the required articles are in, have to be assigned to the variable
page_no = 10


#Automatically loading the next page
for i in range (1,page_no):
    loadMoreButton = driver.find_element_by_class_name('pager-next')
    loadMoreButton.click()
    time.sleep(5)
    print(i)

#seperate the section where the required news articles are in.
main = driver.find_element_by_xpath('//*[@id="content-footer-inside"]/div/div/div')
articleList=[]
#obtaining each news article seperately
articleList = main.find_elements_by_tag_name('li')
len(articleList)
articleList.pop()
len(articleList)

#creating the new variable news
news =[]

r=1
#for loop to extract required variables
for article in articleList:
    news_dict ={}
    print(r)
    r=r+1
    #obtaining header
    header = article.find_element_by_tag_name('span').text
    news_dict['header']= header
    
    #obtaining url 
    url = article.find_element_by_tag_name("a").get_attribute('href')
    news_dict['url'] = url  
    
    #Going inside to that extracted url
    response_url = requests.get(url)
    soup_url = bs(response_url.text)
    
    #Obtaining date
    news_dict['date']=soup_url.select_one('span.datetime').text
    
    #obtaining the full content of the article
    x = soup_url.select('div.content p')
    para = ''.join([element.text for element in x])
    
    news_dict['body']=para


    #appending extracted varibles of each news article into 'news' variable  
    news.append(news_dict)
    
#creating a dataframe         
df = pd.DataFrame(news) 

#appending the website name to the dataframe
df['website_name'] = 'Daily News'

#saving the obtained dataframe 'df' in the 'News Index' folder as a csv file

df.to_csv(r'E:\\News Index\\Daily News_law.csv')  
#The csv file name, 'Daily News_law.csv' in above line should be changed before running the code to extract business and political news articles.
  
    