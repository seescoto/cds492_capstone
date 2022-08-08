# -*- coding: utf-8 -*-
"""
Created on Mon Aug 7 22:17:12 2022

@author: seesc

modelling using processed df
"""

import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

class knn():

    def __init__(self, k = 3, distanceType = 'path'):
        self.k = k
        self.distanceType = distanceType

    def fit(self, xTrain, yTrain):
        self.xTrain = xTrain
        self.yTrain = yTrain

    #knn algorithm for nlp, based off code from towardsdatascience.com
    def predict(self, xTest):
        self.xTest = xTest
        yPred = []

        #find instance thats most similar from training set, then assign same label
        for i in range(len(xTest)):
            maxSim = 0
            index = 0
            for j in range(self.xTrain.shape[0]):
                sim = self.getSimilarity(xTest.loc[i], self.xTrain[j])
                if sim > maxSim:
                    maxSim = temp
                    index = j
            yPred.append(self.yTrain[index])
        return yPred

    def getTag(self, tag):
        #get tag from nltk.pos_tag to wordnet.synsets so similarity can be compared
        tags = {'N' : 'n', 'J' : 'a', 'R' : 'r', 'V' : 'v'}
        return tags.get(tag[0], None) #tag[0] incase list is given

    def toSynsets(self, s):
        #turns string into synset so similarity can be compared
        #tokenizes, tags words, then finds synset for each combo

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

    def getSimilarity(self, s1, s2, distanceType = 'path'):
        #get normalized similarity scale of s1 on s2 (lists)
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

    def getTotalSimilarity(self, string1, string2):
        #averages similarity of s1 on s2 and s2 on s1
        synsets1 = self.toSynsets(string1)
        synsets2 = self.toSynsets(string2)

        return (self.getSimilarity(synsets1, synsets2) + self.getSimilarity(synsets2, synsets1)) / 2
