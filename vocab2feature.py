#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class Vocab2Feature():

    def __init__(self,vocabdata,featureout,methodid = 1):
        self.vocab =  vocabdata;
        self.featureout = featureout 
        self.mid = methodid
        #Key is word, value is a list. First element of list is "list of lists" for every character. Secind element is count of this word
        self.worddict = {}

    #Read the vocabulary file and populate the data worddict 
    def ParseInput(self):
        with open(self.vocab, 'r') as source_data:
            for line in source_data:
                wordtemp = line.split(":")
                word = ''.join(wordtemp[0])
                wordsplits = [[word[:i],word[i:]] for i in range(1,len(word))]
                #Append the word itself to splits, possible cause : entire word is a morpheme
                tmplist = []
                tmplist.append(word)
                wordsplits.append(tmplist)
                if word not in self.worddict: 
                    wordvallist = []
                    wordvallist.append(wordsplits)
                    wordvallist.append(int(wordtemp[1]))
                    self.worddict[word] = wordvallist

    #Helper function 
    def CheckOutput(self):
        for key, val in self.worddict.items():
            print(key,val[0], val[1])


    #Wrapper for generating multiple feature sets
    def ChooseFeature(self):
        if self.mid == 1:
            self.DummyFeature()

    #First-cut dummy feature
    def DummyFeature(self):
        #Key is possible subword, val is count or occurence of each subword in the vocablist
        subworddict = {}
        result_file = open("data/WordSplit.txt", 'w')
        for wordkey,wordval in self.worddict.items(): 
            result_file.write('{0}:{1}\n'.format(wordkey,wordval[0]))
            for subwordlist in wordval[0]:                 
                for subsplit in subwordlist:                    
                    subworddict[subsplit] = subworddict.get(subsplit, 0) + wordval[1]

        
        result_file.close()

        result_file = open(self.featureout, 'w')
        for wordkey,wordval in self.worddict.items():
            flist = []
            for subwordlist in wordval[0]: 
                flstinner = []
                for subsplit in subwordlist:                    
                    flstinner.append(subworddict[subsplit])
                flist.append(flstinner)

            
            result_file.write('{0}:{1}\n'.format(wordkey,flist))

        result_file.close()
        

        



if __name__ == '__main__':
    if len(sys.argv) == 3:
        vocabulary_data = sys.argv[1]
        feature_output = sys.argv[2]
    else:
        vocabulary_data = 'data/vocabulary.txt'
        feature_output = 'data/feature.txt'

    v2f = Vocab2Feature(vocabulary_data,feature_output)
    v2f.ParseInput()    
    v2f.ChooseFeature()


    