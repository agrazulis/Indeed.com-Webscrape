#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 20:08:19 2021

@author: alexandergrazulis
"""

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import boto3
from io import StringIO



# THIS FUNCTION IS MEANT TO DEPLOYED IN AWS LAMBDA FOR THE PURPOSE OF SAVING ARTICLES INTO AN S3 BUCKET
def webscrape(event, context):
##### FINDING DESIRED ELEMENTS FOR ARTICLE TITLES #####
    # Saving URL
    URL = 'https://www.indeed.com/career-advice/search?q=data+science'
    page = requests.get(URL)
    # Pulling data from webpage
    soup = BeautifulSoup(page.content, 'html.parser')
    # Elements we are looking for are in id 'ssr-content'
    results = soup.find(id='ssr-content')
    # Article titles are contained in class 'card'
    articles = results.find_all(class_='card')
    ##### SAVING DF W/ DESIRED ELEMENTS #####
    # Creating column for article title
    Article_Title = [] 
    # Running for loop to pull article titles
    for article in articles:
        # Pulling article names from specified tag & class
        article_elem = article.find('div', class_='card-title h5') 
        if None in (article):
            continue    
        Article_Title.append([article_elem.text.strip()])
    # Saving the article titles in a dataframe
    df = pd.DataFrame(list(zip(Article_Title)), 
            columns =['Article Title'])  
    ##### ADDING COLUMN W/ DATE OF EACH ARTICLE USING REGTEX #####
    # Saving pattern to identify date listed in article heading
    pattern = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})')
    # Saving variable with dates now that pattern has identified them
    pattern_articles = [pattern.findall(article.text) for article in articles ]
    # Adding column to original dataframe
    df['Date'] = pattern_articles
    # Saving article to user-defined s3 bucket
    bucket = 'webscraped-articles'
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, 'df.csv').put(Body=csv_buffer.getvalue())
