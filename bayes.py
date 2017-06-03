from collections import Counter
import csv
import re
import string

with open("neg.csv") as file:
	r_neg = list(csv.reader(file))

with open("pos.csv") as file:
	r_pos = list(csv.reader(file)) 	

print len(r_neg)
print len(r_pos)



def get_text(reviews):
	 return " ".join([r[0].lower() for r in reviews])	



def get_counts(text):
	words = re.split("\s+", text)
	return Counter(words)



def remove_punc(reviews):
	for i in range(len(reviews)):
		for j in range(len(reviews[i])):
			reviews[i][j] = str(reviews[i][j])
			reviews[i][j] = reviews[i][j].translate(None, string.punctuation)


#remove punctuation and get counts for negative text.		
remove_punc(r_neg)
neg_text = get_text(r_neg)
c_neg = get_counts(neg_text)

#remove punctuation and get counts for positive text.

#remove punctuation and get counts for positive text.


print c_neg.most_common(10)



'''
reviews_neg[1][0] = str(reviews_neg[1][0])
reviews_neg[1][0] = reviews_neg[1][0].translate(None, string.punctuation)
print reviews_neg[1][0]
s = "hello it's cole ? ?,."
s = s.translate(None, string.punctuation)
print s
'''