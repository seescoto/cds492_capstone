# CDS492 capstone project
A machine learning model that will predict the truth value of a given statement (whether it is true or false) based on sentiment analysis of previously analyzed statements and Google search results.

Statements with known truth values will be run through an api to scrape the google results of those truth statements. the leading 'snippet', 10 'descriptions', and the number of 'results' will be saved back into the database and then be used with training data (statements that have a snippet, description, and 'results', but no known truth value)

## Installation
The model requires these packages
- numpy
- pandas
- nltk
- scikit-learn
- statistics

To scrape new content from the web as shown in get_data, these packages are required
- requests
- BeautifulSoup
- urllib
- an API key. The one used in api_scrape.py is free for under 1,000 requests per month and can be found [here](https://rapidapi.com/apigeek/api/google-search3/)

To install all required packages (both for modelling and scraping)
```bash
  pip install requirements.txt
```

## Data
the data in the file qa_full.csv has been scraped from websites using the scripts in the get_data folder. Scrape1, scrape2, and scrape3.py collected statements and truth values from various websites and api_scrape.py collected Google snippets, descriptions, and the number of results.

## Contents
- get_data folder contains python scripts used to create the dataset qa_full
- model folder contains python scripts that hold the knn algorithm, that cleaned and pre-processed the data, and that ran the data through the model
- paper folder contains latex files for the technical paper introducing the problem, a literature review, and an explanation as to how the data will be gathered and used.
- results folder contains a .py file that creates visualizations and other data analysis of the model's results, .npy files containing the adjacency matrices of each partition of data, .csv files containing the parititioned datasets, and .txt files containing the test truthValues and their predictions. this is not necessary to run the model yourself, only for me to use so I didn't have to reprocess each partition when I wanted to get more information from it because the knn.process() takes a long time to run
