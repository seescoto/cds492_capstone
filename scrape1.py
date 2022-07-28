# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 14:21:12 2022

@author: seesc

web scraping trivia questions for initial instances of dataset

week3 assignment
2. Continue your technical report (you are welcome to submit the same as you did last
week or a revised report if I asked you so, plus the following):
    
2.1. first exploration of the data (summary statistics, number of variables, 
which are the variables of interest, which you will discard, etc.) (10p)

2.2. the methods you are using and why you are choosing these methods for the 
goal you stated in Week 2 (10p)

2.3. discuss the the pros and cons for the methodology (5p).
"""

import pandas as pd 
import requests 
from bs4 import BeautifulSoup

'''
url ="https://www.opinionstage.com/blog/true-or-false-questions/" 
page = requests.get(url) 

#page.text is the html code, page.content is the html code but in raw bytes
#use raw bytes so theres no problems with encoding

soup = BeautifulSoup(page.content, 'html.parser')
subset = soup.find(id = "post-30302") #part of html with the t/f qs 

#print(subset.prettify())
'''

'''
100 t/f questions from flexiquiz.com
'''

url = "https://www.flexiquiz.com/Help/inspiration/awesome-true-or-false-quiz-questions"
page = requests.get(url) 

soup = BeautifulSoup(page.content, 'html.parser')

#text starts at <ol>, has some headings with style = list-style-type: none
#then questions are <li> ::marker QUESTION <strong>T/F</strong>

blog = soup.find('ol') 
qs = blog.find_all('li')

#take out ones that go <li style= "list-style-type: none">
#those are just titles
questions = []
answers = []
for q in qs:
    q = str(q)
    if "li style=" not in q:
        questions.append(q)
        
#process, split into q and a, string formatting 
for i in range(len(questions)):
    #take out <li></li> from beginning and end 
    questions[i] = questions[i][4:-5]
    
    #split into questions and answers 
    #format is: question - <strong>answer</strong>
    strings = questions[i].split(' <strong>')
    
    #now string[0] = question -, string[1] = answer</strong>
    
    questions[i] = strings[0].strip('-').strip() 
    #strip out hyphens and then trailing whitespaces
    answers.append(strings[1][:-9]) #take out </strong> at end

#create main dataset, 
#will add new ones to this at the end with main.append(df, ignore_index = True)                
main = pd.DataFrame(list(zip(questions, answers)), columns = ['question', 'truthValue'])












   