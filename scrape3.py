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

"""
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

"""
'''
150 t/f questions from momjunction.com

/articles not disallowed on robots.txt, good to scrape
'''

"""
url = "https://www.momjunction.com/articles/true-or-false-questions-for-kids-answers_00695346"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser') 
blog = soup.find_all('p')
"""

#request could not be satisfied, do later


#https://www.momjunction.com/articles/true-or-false-questions-for-kids-answers_00695346/
#get all p, remove any strings that start with 'right answer:' then sort by parity
#questions numbered, split by '.', 1 [1] to get second part aka the question



'''
100 t/f questions for kids at parenting.firstcry.com

/articles allowed (not /articles/author) by robots.txt
'''

url = "https://parenting.firstcry.com/articles/100-awesome-true-or-false-questions-for-kids/"
soup = BeautifulSoup(requests.get(url).content, 'html.parser') 
blog = soup.find_all('p')
#take out last three and first three
blog = blog[3:-3]
print(blog[0])

qs = []
ans = []
for i in range(len(blog)):
    #even index is question , take out number
    #format is #. QESTION
    if i % 2 == 0:
        q = blog[i].text.split('.', 1)[1]
        qs.append(q.strip())
    #odd index is answer, no extra formatting necessary 
    else:
        ans.append(blog[i].text)
    
#print(len(qs) == len(ans))


