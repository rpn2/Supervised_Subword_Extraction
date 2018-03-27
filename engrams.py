def create_engram(word, charcount):
	c = word[charcount]
	if '<' in c or '>' in c:
		return ""
	return word[charcount]
	

def create_forward_bigram(word, charcount):
	bigram = word[charcount:charcount+2]
	if '<' in bigram or '>' in bigram or len(bigram) < 2:
		return ""
	return bigram

def create_backward_bigram(word, charcount):
	bigram = word[charcount:charcount-2:-1]
	if '<' in bigram or '>' in bigram or len(bigram) < 2:
	   return ""
	return bigram

def create_forward_trigram(word, charcount):
	trigram = word[charcount:charcount+3]
	if('<' in trigram or '>' in trigram or len(trigram) < 3):
		return ""
	return trigram

def create_backward_trigram(word, charcount):
	trigram = word[charcount:charcount-3:-1]
	if('<' in trigram or '>' in trigram or len(trigram) < 3):
		return ""
	return trigram


#string = "<onetwothreefourfivesix>"
#for i in range(len(string)):
#	print("Character is " + string[i])
#	print("engram: " + create_engrams(string, i))
#	print("bigram1: " + create_forward_bigrams(string, i))
#	print("bigram2: " + create_backward_bigrams(string, i))
#	print("trigram1: " + create_forward_trigrams(string, i))
#	print("trigram2: " + create_backward_trigrams(string, i))