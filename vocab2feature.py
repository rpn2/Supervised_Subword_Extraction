#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import string
import sys
import math
from datrie import BaseTrie, Trie
import engrams


class Vocab2Feature:

    def __init__(self, vocabulary_data, feature_output, num_features=19, en_ent = 1, en_sw = 1, en_wc = 1, en_ng = 1, en_bg = 1, en_tg = 1):

        self.vocabulary_data = vocabulary_data
        self.feature_output = feature_output
        self.num_features = num_features
        self.word_counts = {}  # Key is word, value is a count of word
        self.featuredict = {}  # key is word, value is list of lists (fetaure vector for each character)

        supported_characters = string.ascii_lowercase + string.digits + '_'
        self.trie = BaseTrie(supported_characters)
        self.reverse_trie = BaseTrie(supported_characters)
        
        self.prefix_entropy = {}  # Key is prefix, value is entropy
        self.reverse_prefix_entropy = {}  

        #Set of enables
        self.en_ent = en_ent
        self.en_sw  = en_sw
        self.en_wc  = en_wc
        self.en_ng  = en_ng        
        self.en_bg  = en_bg
        self.en_tg  = en_tg

    # Parse Input file and store as dictionary
    def parse_input(self):
        total_word_count = 0
        with codecs.open(self.vocabulary_data, 'r', 'utf8') as source_data:
            for line in source_data:
                word, count = line.strip().split(",")
                self.word_counts[word] = int(count)

                self.populate_trie(word=word, prefix_tree=self.trie)
                self.populate_trie(word=word[::-1], prefix_tree=self.reverse_trie)
                total_word_count += 1

        self.generate_template()

    @classmethod
    def populate_trie(cls, word, prefix_tree):
        prefix = u''
        for character in word:
            prefix += character
            prefix_tree.setdefault(prefix, 0)
            prefix_tree[prefix] += 1

    # Generate Feature Vector template
    def generate_template(self):

        for word in self.word_counts.keys():
            chars_word = list(word)
            char_list = []
            for each_char in chars_word:
                char_vector = [None] * self.num_features
                char_list.append(char_vector)
            self.featuredict[word] = char_list

    def write_template(self):
        fp = codecs.open(self.feature_output, 'w', 'utf8')
        fp.write(str(self.featuredict))
        fp.close()


    def calculate_entropy(self):

        for word in self.word_counts.keys(): 
            #word = 'learning'
            prefix = u''            
            for character in word:
                prefix += character
                if prefix not in self.prefix_entropy:
                    slprune = [suffix for suffix in self.trie.suffixes(prefix) if len(suffix) == 1]
                    slval = []
                    if len(slprune):
                        for sl in slprune:
                            tempprefix = prefix + sl
                            slval.append(self.trie[tempprefix])
                        entropy = 0
                        #sumval = sum(slval)
                        for val in slval:
                            entropy =  entropy + (-val/self.trie[prefix])* math.log(val/self.trie[prefix], 2)
                        if sum(slval) < self.trie[prefix]:
                            val = self.trie[prefix] - sum(slval)
                            entropy =  entropy + (-val/self.trie[prefix])* math.log(val/self.trie[prefix], 2)
                        self.prefix_entropy[prefix] = round(entropy,4)
                    else:
                        #This needs to be infinity, could RF handle INF 
                        self.prefix_entropy[prefix] = 0

            reverse_word=word[::-1]
            prefix = u''            
            for character in reverse_word:
                prefix += character
                if prefix not in self.reverse_prefix_entropy:
                    slprune = [suffix for suffix in self.reverse_trie.suffixes(prefix) if len(suffix) == 1]
                    slval = []
                    if len(slprune):
                        for sl in slprune:
                            tempprefix = prefix + sl
                            slval.append(self.reverse_trie[tempprefix])
                        entropy = 0                        
                        for val in slval:
                            entropy =  entropy + (-val/self.reverse_trie[prefix])* math.log(val/self.reverse_trie[prefix], 2)
                        if sum(slval) < self.reverse_trie[prefix]:
                            val = self.reverse_trie[prefix] - sum(slval)
                            entropy =  entropy + (-val/self.reverse_trie[prefix])* math.log(val/self.reverse_trie[prefix], 2)
                        self.reverse_prefix_entropy[prefix] = round(entropy,4)
                    else:
                        #This needs to be infinity, could RF handle INF
                        self.reverse_prefix_entropy[prefix] = 0

    #Populates entropy, subword and wordcount features for every split point in word and reverse_word
    def feature_entropy_subword(self):

        for word,word_count in self.word_counts.items():
            
            char_list = self.featuredict[word]
            reverse_word=word[::-1]   
            revcharcount = len(word) - 2
            #Entropy, sub-word count, wordcount          
            for charcount in range(len(word)):
                feature_index = 0

                char_vector = char_list[charcount]
                beforesp = word[:charcount] if charcount > 0 else ' '
                currsp   = word [:charcount+1]
                aftersp  = word[:charcount+2] if charcount < (len(word) - 1) else ' '

                #Entropy, sub-word count for reverse
                rev_beforesp = reverse_word[:revcharcount] if revcharcount > 0 else ' '
                rev_currsp   = reverse_word [:revcharcount+1]
                rev_aftersp  = reverse_word[:revcharcount+2] if revcharcount < (len(word) - 1) else ' '

                #populate entropy

                if (self.en_ent == 1):
                    char_vector[feature_index]  = self.prefix_entropy.get(u''+ beforesp,0)
                    feature_index += 1
                    char_vector[feature_index]  = self.prefix_entropy.get(u''+ currsp)
                    feature_index += 1
                    char_vector[feature_index]  = self.prefix_entropy.get(u''+ aftersp,0)
                    feature_index += 1               

                    char_vector[feature_index]  = self.reverse_prefix_entropy.get(u''+ rev_beforesp,0)
                    feature_index += 1
                    char_vector[feature_index]  = self.reverse_prefix_entropy.get(u''+ rev_currsp,0)
                    feature_index += 1
                    char_vector[feature_index]  = self.reverse_prefix_entropy.get(u''+ rev_aftersp,0)
                    feature_index += 1    
                
                #populate subword count

                if (self.en_sw == 1):
                    char_vector[feature_index]  = self.trie.get(u''+ beforesp,0)
                    feature_index += 1
                    char_vector[feature_index]  = self.trie.get(u''+ currsp)
                    feature_index += 1
                    char_vector[feature_index]  = self.trie.get(u''+ aftersp,0) 
                    feature_index += 1     

                    char_vector[feature_index]   = self.reverse_trie.get(u''+ rev_beforesp,0)
                    feature_index += 1
                    char_vector[feature_index]  = self.reverse_trie.get(u''+ rev_currsp,0)
                    feature_index += 1
                    char_vector[feature_index]  = self.reverse_trie.get(u''+ rev_aftersp,0)
                    feature_index += 1           
                              

                ##populate wordcount
                if (self.en_wc == 1):
                    char_vector[feature_index] = word_count
                    feature_index += 1 

                #populate engram, bigrams, trigrams
                if (self.en_ng == 1):
                    char_vector[feature_index] = engrams.create_forward_engram(word, charcount)
                    feature_index += 1
                    char_vector[feature_index] = engrams.create_backward_engram(word, charcount)
                    feature_index += 1

                if (self.en_bg == 1):
                    char_vector[feature_index] = engrams.create_forward_bigram(word, charcount)
                    feature_index += 1
                    char_vector[feature_index] = engrams.create_backward_bigram(word, charcount)
                    feature_index += 1

                if (self.en_tg == 1):
                    char_vector[feature_index] = engrams.create_forward_trigram(word, charcount)
                    feature_index += 1
                    char_vector[feature_index] = engrams.create_backward_trigram(word, charcount)
                    feature_index += 1
                
                char_list[charcount] = char_vector
                revcharcount = revcharcount - 1

            self.featuredict[word] = char_list


    # Helper functions
    def check_worddict(self):

        for key, val in self.word_counts.items():
            print(key, val)

    def check_featuredict(self):

        fp = codecs.open(self.feature_output, 'w', 'utf8')
        fp.write(str(self.featuredict))
        fp.close()

    def check_entropy(self):
        print(len(self.prefix_entropy))
        fp = codecs.open("data/debugentropy", 'w', 'utf8')
        fp.write(str(self.prefix_entropy))
        fp.close()

        print(len(self.reverse_prefix_entropy))
        fp = codecs.open("data/reversedebugentropy", 'w', 'utf8')
        fp.write(str(self.reverse_prefix_entropy))
        fp.close()


if __name__ == '__main__':

    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = 'data/combined_vocabulary.txt'
        output_file = 'data/populated_feature.txt'

    #vocabulary_data, feature_output, num_features=19, en_ent = 1, en_sw = 1, en_wc = 1, en_ng = 1, en_bg = 1, en_tg = 1
    v2f = Vocab2Feature(input_file,output_file,14,1,1,0,1,0,0)
    v2f.parse_input()
    v2f.calculate_entropy()
    v2f.feature_entropy_subword()
    v2f.check_featuredict()
    #v2f.check_entropy()
    



