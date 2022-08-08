#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 23:55:52 2022

@author: sofiaescoto

data cleaning, collecting data snippets for the cnn with a web search api
"""

import pandas as pd
import urllib
import requests
import config #api-key


#using a free api with 1000 scrapes / month for original scrape (by apigeek)
#using a different free api with 100 scrapes / day for app implementation of model (by contextualwebsearch)
df = pd.read_csv('qa.csv')
df = df[['question','truthValue']] #get rid index cols

#find any na's
#print(df.isnull().values.sum())
#print(df[df.isnull().any(axis = 1)])
#row 170 has na question and tv, just remove
df = df.dropna()

#check tv values, should only have true and false
#print(df['truthValue'].unique())
#replace with bool using str.contains (no case sensitivity)
df.loc[df['truthValue'].str.contains('True', case = False, na = False), 'truthValue'] = True
df.loc[df['truthValue'].str.contains('False', case = False, na = False), 'truthValue'] = False


'''
headers = {"x-rapidapi-key": config.api_key,
           "x-rapidapi-host" :"google-search3.p.rapidapi.com"}

query = {"q": df['question'][0],
         "num" : 20}

results = requests.get("https://rapidapi.p.rapidapi.com/api/v1/search/" + urllib.parse.urlencode(query),
                   headers = headers)
results = results.json()
print(results)

#results['featured_snippet']['featured_snippet']
#also for i in results['results']:
    #i['description'] (only if not empty)

'''

#now go through all values in the dataframe and add featured_snippet + descriptions

headers = {"x-rapidapi-key": config.api_key,
           "x-rapidapi-host" :"google-search3.p.rapidapi.com"}

snips = []
descs = []
nums = []
for i in range(len(df)):

    #key error at 170, just skip it
    if i != 170:
        query = {'q': df['question'][i]}
        results = requests.get("https://rapidapi.p.rapidapi.com/api/v1/search/" +
                               urllib.parse.urlencode(query), headers = headers)
        results = results.json()

        #snippet column
        if 'featured_snippet' in results.keys():
            snippet = results['featured_snippet']['featured_snippet']
            snips.append(snippet)
        else:
            snips.append(None)

        #description column
        description = ""
        for j in results['results']:
            d = j['description']
            if len(d) > 3:#so even just the word 'true' could be added if needed
                description += d + "\n"
        descs.append(description)

        #total results
        nums.append(results['total'])


df = df.reindex(index = range(573))

df['snippet'] = snips
df['description'] = descs
df['results'] = nums

cds df.to_csv('qa_full.csv', index = False)

'''
#error halfway through when i = 170, prob from removed na
halfDoneDf = df[0:170]
halfDoneDf['snippet'] = snips
halfDoneDf['description'] = descs
halfDoneDf['results'] = nums

halfDoneDf.to_csv('half_qa.csv')
'''
