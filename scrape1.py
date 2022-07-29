# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 14:21:12 2022

@author: seesc

web scraping trivia questions for initial instances of dataset
first two websites, 200 t/f questions given

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
100 t/f questions from flexiquiz.com
/help not disallowed in robots.txt, good to scrape
'''

url = "https://www.flexiquiz.com/Help/inspiration/awesome-true-or-false-quiz-questions"
page = requests.get(url) 

soup = BeautifulSoup(page.content, 'html.parser')
#page.text is the html code, page.content is the html code but in raw bytes
#use raw bytes so theres no problems with encoding

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
    answers.append(strings[1].strip().strip('<br/>').strip().strip("</strong>")) 
    #take out <br/> and </strong> at end if there (plus spaces)

#create main dataset, 
#will add new ones to this at the end with main.append(df, ignore_index = True)                
main = pd.DataFrame(list(zip(questions, answers)), columns = ['question', 'truthValue'])


'''
100 t/f questions from signupgenius
/groups not disallowed in robots.txt, good to scrape
'''
url = "https://www.signupgenius.com/groups/true-or-false-questions.cfm"
page =requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#all q's are in <td class = "main"
blog = soup.find('td', class_ = 'main')
qs = blog.find_all('ol') #questions all in <ol>
ans = blog.find_all('p') #ansers all in <p>
questions = []
answers = []

#some values in <p> are just headers, not answers, remove if class = 'body-sample-link'
#jk, some non-answers dont have that, but all answers have p style="margin-left: 40px;"

for a in ans:
    if "p style=" in str(a):
        answers.append(a)
        
#print(len(answers) == len(qs))
#true - both same length, can continue to string formatting 

#text removes markdown automatically, strip() is normal whitespace removal
for i in range(len(qs)):
    questions.append(qs[i].text.strip())
    answers[i] = answers[i].text.strip()
    
    #remove periods & whitespaces from questions
    questions[i] = questions[i].strip('.').strip()
    
    #answers are in format "Answer: TRUTHVALUE - EXPLANATION" 
    #only want truth value
    answers[i] = answers[i].split('-', 1)[0] #just Answer: TRUTHVALUE
    answers[i] = answers[i].split('Answer:')[1] #just TRUTHVALUE
    answers[i] = answers[i].strip()

    #ISSUE!!! if two dashes in answer, second one used. not sure why bc/ split
    #should fix that by putting 1 as an arg
    #will fix when its not 5am 

#create second dataset
df = pd.DataFrame(list(zip(questions, answers)), columns = ['question', 'truthValue'])

main = main.append(df, ignore_index = True)

#export to csv
main.to_csv('qa.csv')

   