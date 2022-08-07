#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 22:58:11 2022

@author: sofiaescoto

scrape 3 - t/f questions
"""

import pandas as pd 
import requests
from bs4 import BeautifulSoup 

'''
45 t/f general knowledge q's from bigquizthing.com

robots.txt doesnt disallow anything, good to scrape
'''


url = "https://bigquizthing.com/trivia-questions-ans/general-knowledge-45-true-or-false-questions-and-answers/"
page = requests.get(url) 
soup = BeautifulSoup(page.content, 'html.parser')

ps = soup.find_all('p')

ps = ps[3:-4] #skip first three and last four 
#remove image in article
        
all_ps = [p for p in ps if "img" not in str(p)]    


qs = [] 
ans = [] 

for i in range(len(all_ps)):
    #evens are questions
    if i % 2 == 0:
        qs.append(all_ps[i].text.strip().strip('.').strip('?').strip())
    #odds are answers 
    else:
        a = all_ps[i].text
        #format is Answer: TRUTHVALUE. explation
        a = a.strip("Answer:") #TRUTHVALUE. explanation
        a = a.split('.', 1)[0] #just truthvalue
        ans.append(a.strip())
        
#print(len(qs) == len(ans))

df1 = pd.DataFrame(list(zip(qs, ans)), columns = ['question', 'truthValue'])




'''
100 t/f questions for kids at parenting.firstcry.com

/articles allowed (not /articles/author) by robots.txt
'''

url = "https://parenting.firstcry.com/articles/100-awesome-true-or-false-questions-for-kids/"
soup = BeautifulSoup(requests.get(url).content, 'html.parser') 
blog = soup.find_all('p')
#take out last three and first three
blog = blog[3:-3]

qs = []
ans = []
for i in range(len(blog)):
    #even index is question , take out number
    #format is #. QUESTION
    if i % 2 == 0:
        q = blog[i].text.split('.', 1)[1]
        qs.append(q.strip())
    #odd index is answer, no extra formatting necessary 
    else:
        ans.append(blog[i].text)

#print(len(qs) == len(ans))

        
df2 = pd.DataFrame(list(zip(qs, ans)), columns = ['question', 'truthValue'])


'''
60 t/f questions from ponly.com 

only /wp-admin disallowed on robots.txt, good to scrape
'''

url = "https://ponly.com/true-or-false-questions/"
soup = BeautifulSoup(requests.get(url).content, 'html.parser')
blog = soup.find('div', class_ = "entry-content")
ps = blog.find_all('p')

#skip first 7 and last two
ps = ps[7:-2]

#questions format: #. QUESTION
#answers format: A: True
#or 
#A: False. explanation
#also some empty strings with just a space, .text makes it \xa0

ps = [p for p in ps if p.text != "\xa0"]
qs = [] 
ans = []

#some extra tags (5), sort by if contains A: or next p contants A:
for i in range(len(ps)):
    if (i + 1 < len(ps)) and (ps[i+1].text.startswith('A:')):
        q = ps[i].text.split('.', 1)[1] #get after number
        qs.append(q.strip())
    elif ps[i].text.startswith('A:'):
        a = ps[i].text.replace('A: ','')
        a = a.split('.')[0]
        ans.append(a.strip())
    else:
        continue
    
    
    
df3 = pd.DataFrame(list(zip(qs, ans)), columns = ['question', 'truthValue'])
 
#get csv, merge, export back to csv               
main = pd.read_csv('qa.csv') 
main = pd.concat([main, df1, df2, df3], ignore_index = True)
main.to_csv('qa.csv')
        
        
        
        