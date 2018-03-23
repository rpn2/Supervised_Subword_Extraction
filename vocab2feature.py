#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import string
import sys
import math
from datrie import BaseTrie, Trie


class Vocab2Feature:

    def __init__(self, vocabulary_data, feature_output, num_features=19):

        self.vocabulary_data = vocabulary_data
        self.feature_output = feature_output
        self.num_features = num_features
        self.word_counts = {}  # Key is word, value is a count of word
        self.featuredict = {}  # key is word, value is list of lists (fetaure vector for each character)

        supported_characters = string.ascii_lowercase + string.digits + '_'
        self.trie = BaseTrie(supported_characters)
        self.reverse_trie = BaseTrie(supported_characters)
        
        self.prefix_entropy = {}  # Key is prefix, value is entropy, Basetrie or trie does not store float, so use normal dictionary for entropy
        self.reverse_prefix_entropy = {}  # Key is prefix, value is entropy

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

    # Populate global character count as dummy fetaure, index is location in feature vector
    #To be removed in final version, just a template
    def dummy_charcount(self, index):

        char_count = {}
        for word, count in self.word_counts.items():
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
        fp.write(str(self.featuredict))
        fp.close()

    def calculate_entropy(self):

        for word in self.word_counts.keys():            
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
                        sumval = sum(slval)
                        for val in slval:
                            entropy =  entropy + (-val/sumval)* math.log(val/sumval, 2)
                        self.prefix_entropy[prefix] = entropy
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
                        sumval = sum(slval)
                        for val in slval:
                            entropy =  entropy + (-val/sumval)* math.log(val/sumval, 2)
                        self.reverse_prefix_entropy[prefix] = entropy
                    else:
                        #This needs to be infinity, could RF handle INF
                        self.reverse_prefix_entropy[prefix] = 0

    #Populates entropy, subword and wordcount features for every split point in word and reverse_word
    def feature_entropy_subword(self):

        for word,word_count in self.word_counts.items():
            
            char_list = self.featuredict[word]
            reverse_word=word[::-1]   
            revcharcount = len(word) - 1
            #Entropy, sub-word count, wordcount          
            for charcount in range(len(word)):
                char_vector = char_list[charcount]
                beforesp = word[:charcount] if charcount > 0 else ' '
                currsp   = word [:charcount+1]
                aftersp  = word[:charcount+2] if charcount < (len(word) - 1) else ' '

                #populate entropy
                char_vector[0]  = self.prefix_entropy.get(u''+ beforesp,0)
                char_vector[1]  = self.prefix_entropy.get(u''+ currsp)
                char_vector[2]  = self.prefix_entropy.get(u''+ aftersp,0)                
                
                #populate subword count
                char_vector[6]  = self.trie.get(u''+ beforesp,0)
                char_vector[7]  = self.trie.get(u''+ currsp)
                char_vector[8]  = self.trie.get(u''+ aftersp,0) 
                
                #populate wordcount
                char_vector[12] = word_count               

                #Entropy, sub-word count for reverse
                rev_beforesp = reverse_word[:revcharcount] if revcharcount > 0 else ' '
                rev_currsp   = reverse_word [:revcharcount+1]
                rev_aftersp  = reverse_word[:revcharcount+2] if revcharcount < (len(word) - 1) else ' '

                #populate entropy
                char_vector[3]  = self.reverse_prefix_entropy.get(u''+ rev_beforesp,0)
                char_vector[4]  = self.reverse_prefix_entropy.get(u''+ rev_currsp)
                char_vector[5]  = self.reverse_prefix_entropy.get(u''+ rev_aftersp,0)                
                
                #populate subword count
                char_vector[9]   = self.reverse_trie.get(u''+ rev_beforesp,0)
                char_vector[10]  = self.reverse_trie.get(u''+ rev_currsp)
                char_vector[11]  = self.reverse_trie.get(u''+ rev_aftersp,0)
                
                char_list[charcount] = char_vector
                revcharcount = revcharcount - 1

            self.featuredict[word] = char_list


    # Helper functions
    def check_worddict(self):

        for key, val in self.word_counts.items():
            print(key, val)

    def check_featuredict(self):

        fp = codecs.open("data/populatedfeature.txt", 'w', 'utf8')
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
        input_file = 'data/updated_vocabulary.txt'
        output_file = 'data/feature.txt'

    v2f = Vocab2Feature(input_file, output_file)
    v2f.parse_input()
    v2f.calculate_entropy()
    v2f.feature_entropy_subword()
    v2f.check_featuredict()
    #v2f.check_entropy()
    '''v2f.write_template()
    v2f.dummy_charcount(0)
    v2f.dummy_charcount(1)
    v2f.dummy_charcount(2)
    v2f.dummy_charcount(3)'''



