def create_forward_engram(word, charcount):
	return word[charcount + 1] if charcount + 2 != len(word) else word[charcount + 1] + ">"

def create_backward_engram(word, charcount):
	return word[charcount] if charcount != 0 else "<" + word[charcount]

def create_forward_bigram(word, charcount):
	bigram = word[charcount+1 : charcount+3]
	if len(bigram) < 2:
		return ""
	if charcount + 3 == len(word):
		return bigram + ">"
	return bigram

def create_backward_bigram(word, charcount):
	bigram = word[charcount : None if charcount - 2 == -1 else charcount -2  : -1]
	if len(bigram) < 2:
	   return ""
	if charcount - 2 == -1:
		return bigram + ">"
	return bigram

def create_forward_trigram(word, charcount):
	trigram = word[charcount+1 : charcount+4]
	if len(trigram) < 3:
		return ""
	if charcount + 4 == len(word):
		return trigram + ">"
	return trigram

def create_backward_trigram(word, charcount):
	trigram = word[charcount: None if charcount - 3 == -1 else charcount -3 : -1]
	if len(trigram) < 3:
		return ""
	if charcount - 3 == -1:
		return trigram + ">"
	return trigram


string = "onetwothreefourfivesix"
#for i in range(len(string) - 1):
#	print("Splitpoint is between " + string[i] + " and " + string[i + 1])
#	print("____________________________________")
#	print("engram1: " + create_forward_engram(string, i))
#	print("engram2: " + create_backward_engram(string, i))
#	print("bigram1: " + create_forward_bigram(string, i))
#	print("bigram2: " + create_backward_bigram(string, i))
#	print("trigram1: " + create_forward_trigram(string, i))
#	print("trigram2: " + create_backward_trigram(string, i))
#	print("____________________________________")