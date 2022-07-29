# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 11:43:09 2022

@author: seesc

scrape 2 - t/f questions
"""

import pandas as pd 
import requests
from bs4 import BeautifulSoup

'''
100 t/f questions from playosmo.com

/kids-learning not disallowed on robots.txt (only /kids-learning/xmlrpc.php) 
so good to scrape
'''

url = "https://www.playosmo.com/kids-learning/true-or-false-questions-for-kids/"
page = requests.get(url) 
soup = BeautifulSoup(page.content, 'html.parser') 

blog = soup.find('ol')
#questions in <li>, answers in <p>
qs = blog.find_all('li')
ans = blog.find_all('p')
#answer format = <strong>Answer:</strong> TRUTHVALUE

#print(len(ans) == len(qs))

questions = [] 
answers = []  

for i in range(len(qs)):
    questions.append(qs[i].text.strip('.').strip())
    answers.append(ans[i].text.strip())
    
    answers[i] = answers[i].split('Answer: ')[-1] #get end of string after answer: 
    
df3 = pd.DataFrame(list(zip(questions, answers)), columns = ['question', 'truthValue'])  

'''
70 t/f questions from cosmopolitan.com

/uk/worklife not disallowed on robots.txt, good to scrape

'''      

url = "https://www.cosmopolitan.com/uk/worklife/a32612392/best-true-false-quiz-questions/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser') 

#questions and answers in separate sections, but both in ol class = "body-ol"
blog = soup.find_all('ol', class_ = "body-ol") 

questions = [] #format fine
answers = [] #format = TRUTHVALUE - explanation

#tried to use indeces so i could use one for loop but kept getting errors
#so i used two just for the sake of time
for q in blog[0]:
    questions.append(q.text.strip('.').strip()) 

for a in blog[1]:
    answers.append(a.text.split('-')[0].strip())

df4 = pd.DataFrame(list(zip(questions, answers)), columns = ['question', 'truthValue']) 

main = pd.concat([df3, df4], ignore_index = True)


