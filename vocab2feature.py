#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


class Vocab2Feature():


    def __init__(self,vocabulary_data,feature_output,num_features = 4):

        self.vocabulary_data =  vocabulary_data
        self.feature_output = feature_output 
        self.num_features = num_features                                    
        self.worddict = {}  #Key is word, value is a count of word
        self.featuredict = {}  #key is word, value is list of lists (fetaure vector for each character)

    #Parse Input file and store as dictionary
    def parse_input(self):

        with open(self.vocabulary_data, 'r') as source_data:
            for line in source_data:
                wordtemp = line.split(":")  
                self.worddict[wordtemp[0]] = int(wordtemp[1])
        self.generate_template()

    #Generate Feature Vector template
    def generate_template(self):

        for word in self.worddict.keys():
            chars_word = list(word)
            char_list = []
            for each_char in chars_word:
                char_vector = [None] * self.num_features
                char_list.append(char_vector)
            self.featuredict[word] = char_list

    def write_template(self):

        fp = open(self.feature_output, 'w')
        fp.write( str(self.featuredict) )
        fp.close()

    #Populate global character count as dummy fetaure, index is location in feature vector
    def dummy_charcount(self, index):

        char_count = {}
        for word, count in self.worddict.items():
            chars_word = list(word)
            for each_char in chars_word:
                char_count[each_char] = char_count.get(each_char, 0) + count

        for word, value in self.featuredict.items():
            chars_word = list(word)
            char_list = []
            for charindex in range(len(chars_word)):
                char_vector = value[charindex]
                char_vector[index] = char_count[chars_word[charindex]]
                char_list.append(char_vector)

            self.featuredict[word] = char_list

        fp = open("data/dummyfeature.txt", 'w')
        fp.write( str(self.featuredict) )
        fp.close()

    #Helper functions
    def check_worddict(self):

        for key, val in self.worddict.items():
            print(key,val)

    def check_featuredict(self):

        for key, val in self.featuredict.items():
            print(key,val)


if __name__ == '__main__':

    if len(sys.argv) == 3:
        vocabulary_data = sys.argv[1]
        feature_output = sys.argv[2]
    else:
        vocabulary_data = 'data/vocabulary.txt'
        feature_output = 'data/feature.txt'

    v2f = Vocab2Feature(vocabulary_data,feature_output)
    v2f.parse_input() 
    v2f.write_template()
    v2f.dummy_charcount(0)
    v2f.dummy_charcount(1)
    v2f.dummy_charcount(2)
    v2f.dummy_charcount(3)
    


