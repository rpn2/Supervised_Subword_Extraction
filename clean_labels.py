
import codecs
import re

k =0
word_label = {}

word_list = {}
word_cnt = {}

with open('data/roots.txt', 'r') as source_data:
    for data in source_data:        
        datalist = data.split()
        if len(datalist) > 0:
            word = re.sub('[^0-9a-z\-]+', '', datalist[0].lower()).replace('-', "_")
            if word not in word_list:
                word_list[word] = datalist[1:] 
                word_cnt[word] = 1
            else:
                word_list[word] = word_list.get(word,[]) + datalist[1:]
                word_cnt[word] = word_cnt[word] + 1
    
clean_up = {}
zero_length = {}

for word, labellist in word_list.items():
    found = 0
    modlist = sorted(labellist, key=len)[::-1]       
    if len(modlist) > 0:
        for subword in modlist:
            loc = word.find(subword)
            if loc != -1:
                label_index = []
                for i in range(len(word)):
                    label_index.append(i)                    
                    if (loc - 1) == i:
                        label_index.append(1)
                    elif loc + len(subword)-1 == i:
                        label_index.append(1)
                    else:
                        label_index.append(0)
                word_label[word] = label_index
                found = 1
                break
        if found == 0:
            clean_up[word] = labellist


    else:
        label_index = []
        for i in range(len(word)):
            label_index.append(i)
            label_index.append(0)
        word_label[word] = label_index
        zero_length[word] = 1

        
fp = codecs.open("data/zero_length.txt", 'w', 'utf8')
fp.write(str(clean_up))
fp.close()

fp = codecs.open("data/labels_data.txt", 'w', 'utf8')
fp.write(str(word_list))
fp.close()



fp = codecs.open("data/labels_dict.txt", 'w', 'utf8')
fp.write(str(word_label))
fp.close()

print(len(word_label))



vocab_count = {}
with codecs.open("data/updated_vocabulary.txt", 'r', 'utf8') as source_data:
    for line in source_data:
        word, count = line.strip().split(",")
        vocab_count[word] = count



result_file = codecs.open("data/combined_vocabulary.txt", 'w', 'utf8')
for word,count in vocab_count.items():
    result_file.write('{0},{1}\n'.format(word, count))

cnt = 0
for word,count in word_cnt.items():
    if word not in vocab_count:
        result_file.write('{0},{1}\n'.format(word, count))
        cnt += 1

result_file.close()

print(cnt)









        


