def create_forward_engram(word, charcount):
	return word[charcount + 1] if charcount + 1 != len(word) else  ">"

def create_backward_engram(word, charcount):
	return word[charcount] 

def create_forward_bigram(word, charcount):
	bigram = word[charcount+1 : charcount+3]
	if len(bigram) == 0:
		return ">"
	return bigram

def create_backward_bigram(word, charcount):
	bigram = word[charcount - 1 : charcount + 1] if charcount -1 >= 0 else word[0: charcount + 1]
	
	return bigram

def create_forward_trigram(word, charcount):
	trigram = word[charcount+1 : charcount+4]
	if len(trigram) == 0:
		return ">"
	return trigram

def create_backward_trigram(word, charcount):
	trigram = word[charcount - 2 : charcount + 1] if charcount -2 >= 0 else word[0: charcount + 1]
	
	return trigram


'''string = "learning"
for i in range(len(string)):
	print("____________________________________")
	print("engram1: " + create_forward_engram(string, i))
	print("engram2: " + create_backward_engram(string, i))
	print("bigram1: " + create_forward_bigram(string, i))
	print("bigram2: " + create_backward_bigram(string, i))
	print("trigram1: " + create_forward_trigram(string, i))
	print("trigram2: " + create_backward_trigram(string, i))
	print("____________________________________")'''