# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 01:43:26 2022

@author: seesc

knn() model class - uses already processed dataframe (gone through clean())
"""

import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
import statistics as stat

#knn algorithm for nlp, partially based off code from towardsdatascience.com
class knn():

    def __init__(self, k = 3, distanceType = 'path'):
        self.k = k
        self.distanceType = distanceType

    def fit(self, xTrain, yTrain):
        self.xTrain = xTrain
        self.yTrain = yTrain

    def process(self, xTest):
        self.xTest = xTest
        self.adjMatrix = np.empty([len(self.xTest), len(self.xTrain)], dtype = object)

        #create adjMatrix so no need to re-calculate with k > 1
        for i in range(len(self.xTest)):
            for j in range(len(self.xTrain)):
                sim = self.getStringSimilarity(self.xTest.iloc[i], self.xTrain.iloc[j])
                self.adjMatrix[i][j] = [sim, j]

    def predict(self):
        yPred = []

        #find instances thats most similar from training set, then assign same label
        for i in range(len(self.xTest)):
            yPred.append(self.predictEach(i))
        return yPred

    def predictEach(self, row):
        #predicts each row (instance) using k neighbors

        #find first k maxes in the row
        maxes = self.getKMaxes(self.adjMatrix[row])

         #return most common answer for neighbors
         #if a tie for most common return most common of k-1 neighbors
         #else return most similar (first neighbor) (won't be a prob with t/f but future proofing)
        try:
          return(stat.mode(maxes))
        except:
          try:
            return(stat.mode(maxes[-1:]))
          except:
            return(maxes[0])

    def getKMaxes(self, similarities):

        #returns k of the biggest similarity scores to
        similarities = similarities.tolist()
        maxes = []
        for k in range(self.k):
            m = max(similarities)
            similarities.remove(m) #remove that index
            maxes.append(m)

        #each item in maxes is formatted [similarity_score (float), col (index from yTrain, int)]

        #get t/f values
        truthValues = []
        for i in maxes:
            #col = i[-1]
            truthValues.append(self.yTrain.iloc[i[1]]) #just truthValue

        return truthValues

    #provided by towardsdatascience
    def getTag(self, tag):
        #get tag from nltk.pos_tag to wordnet.synsets so similarity can be compared
        tags = {'N' : 'n', 'J' : 'a', 'R' : 'r', 'V' : 'v'}
        return tags.get(tag[0], None) #tag[0] incase list is given

    #provided by towardsdatascience
    def toSynsets(self, s):
        #turns string into synset so similarity can be compared
        #tokenizes, tags words, then finds synset for each combo

        s = ' '.join(str(x) for x in list(s))
        words = word_tokenize(s + ' ')

        synsets = []
        if len(words) == 1:
            tags = nltk.pos_tag(words[0] + ' ')
        else:
            tags = nltk.pos_tag(words)

        for word, tag in zip(words, tags):
            synTag = self.getTag(tag[1])
            syns = wn.synsets(word, synTag)
            if len(syns) > 0:
                synsets.append(syns[0])

        return synsets

    #provided by towardsdatascience
    def getSimilarity(self, s1, s2, distanceType = 'path'):
        #get normalized similarity scale of s1 on s2 (lists of synsets)
        #s1 and s2 max similarities for all, sum and find mean

        s1Scores = []

        for i, s1Synset in enumerate(s1, 0):
            maxScore = 0
            for s2Synset in s2:
                if distanceType == 'path':
                    score = s1Synset.path_similarity(s2Synset, simulate_root = False)
                else:
                    score = s1Synset.wup_similarity(s2Synset)
                if (score != None) and (score > maxScore):
                    maxScore = score

            if maxScore != 0:
                s1Scores.append(maxScore)

        normScore = np.mean(s1Scores)
        return normScore

    def getStringSimilarity(self, string1, string2):
        #averages similarity of s1 on s2 AND s2 on s1
        s1 = self.toSynsets(string1)
        s2 = self.toSynsets(string2)
        return (self.getSimilarity(s1, s2) + self.getSimilarity(s2, s1) / 2)
