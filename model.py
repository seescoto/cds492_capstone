# -*- coding: utf-8 -*-
"""
Created on Mon Aug 7 22:17:12 2022

@author: seesc

modelling using processed df
"""

class knn():
    def __init__(self, k = 3, distanceType = 'path'):
        self.k = k
        self.distanceType = distanceType

    def fit(self, xTrain, yTrain):
        self.xTrain = xTrain
        self.yTrain = yTrain

    #knn algorithm for nlp, based off code from towardsdatascience.com
    def predict(self, xTest):
        self.xTest =xTest
        yPred = []

        #find instance thats most similar from training set, then assign same label
        for i in range(len(xTest)):
            maxSim = 0
            index = 0
            for j in range(self.xTrain.shape[0]):
                sim = self.document_similarity(xTest[i], self.xTrain[j])
                if sim > maxSim:
                    maxSim = temp
                    index = j
            yPred.append(self.yTrain[index])
        return yPred

    def getTag(self, tag):
        #get tag from nltk.pos_tag to wordnet.synsets so similarity can be compared
        tags = {'N' : 'n', 'J' : 'a', 'R' : 'r', 'V' : 'v'}
        return tags.get(tag[0], None) #tag[0] incase list is given

    def toSynsets(self, string):
        #turns string into synset so similarity can be compared
        #tokenizes, tags words, then finds synset for each combo

        words = word_tokenize(string + ' ')

        synsets = []
        if len(words) == 1:
            tags = nltk.pos_tag(words[0] + ' ')
        else:
            
