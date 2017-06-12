from __future__ import division
from collections import Counter
import csv
import re
import string
import time
import sys

def get_text(reviews):
	 #for small files, (neg.csv and pos.csv)
	 #return " ".join([r[0].lower() for r in reviews])
	 
	text = " "
	for row in range(len(reviews)):
		s = "".join(reviews[row])
		text += "".join(s.lower())
		text += " "


	return text	
	 

def get_counts(text):
	words = re.split("\s+", text)
	return Counter(words)



def remove_punc(reviews):
	for i in range(len(reviews)):
		for j in range(len(reviews[i])):
			reviews[i][j] = str(reviews[i][j])
			reviews[i][j] = reviews[i][j].translate(None, string.punctuation)



def train(total_words, total_pos_words, total_neg_words, counter_p, counter_n):
	start_time = time.time()
	print "Starting to train classifer"

	feat_prob_neg = dict(counter_n)
	feat_prob_pos = dict(counter_p)

	for feature in counter_n:
		feature_count = counter_n[feature]
		feat_prob_neg[feature] = float((feature_count+1)/total_words)
	

	for feature in counter_p:
		feature_count = counter_p[feature]
		feat_prob_pos[feature] = float((feature_count+1)/total_words)

	print("The classifier is trained and it took %s seconds" % (time.time() - start_time))

	return feat_prob_pos, feat_prob_neg

	

def make_class_prediction(review, unique_class_feat, prob_class, feat_probs_class, num_reviews_in_class, common_words):
	prediction = 1
	
	for word in range(len(review)):
		feat = review[word]
		if(feat in feat_probs_class.keys()):
			#NEW: Data for words like "the" and "and" are heavily favoured to one side. Remove these words.
			
			if(feat in common_words.keys()):
				prediction *= (1/unique_class_feat)	
			else:
				prediction *= feat_probs_class[feat]
		else:
			
			prediction *= (1/unique_class_feat)	


	prediction /= (unique_class_feat + num_reviews_in_class)
	prediction *= prob_class		

	return prediction



def test_data():

	# ************************************************************
	# ***************** TESTING NOW  ****************************


	test_neg_time = time.time()
	print "Training done. Testing Negative Reviews now."
	# ***************** NEGATIVE ********************************
	remove_punc(reviews_neg_test)
	final_predictions_neg = []


	for row in range(len(reviews_neg_test)):
		s = ''.join(reviews_neg_test[row])
		s = s.split()
		predict_neg = make_class_prediction(s, unique_neg, prob_class_neg, feat_prob_neg, num_neg_reviews, neg_common)
		predict_pos = make_class_prediction(s, unique_pos, prob_class_pos, feat_prob_pos, num_pos_reviews, pos_common)

		if (predict_neg > predict_pos):
			final_predictions_neg.append("Negative")
		else:
			final_predictions_neg.append("Positive")

	print("Predictions for negative reviews finished in %s seconds" % (time.time() - test_neg_time))		




	test_pos_time = time.time()
	print "Testing Negative Reviews done. Testing Positive Reviews now."
	# ***************** POSITIVE ********************************
	remove_punc(reviews_pos_test)
	final_predictions_pos = []


	for row in range(len(reviews_pos_test)):
		s = ''.join(reviews_pos_test[row])
		s = s.lower()
		s = s.split()
		predict_neg = make_class_prediction(s, unique_neg, prob_class_neg, feat_prob_neg, num_neg_reviews, neg_common)
		predict_pos = make_class_prediction(s, unique_pos, prob_class_pos, feat_prob_pos, num_pos_reviews, pos_common)

		if (predict_neg > predict_pos):
			final_predictions_pos.append("Negative")
		else:
			final_predictions_pos.append("Positive")	

	print("Predictions for positive reviews finished in %s seconds" % (time.time() - test_pos_time))

	neg_results = Counter(final_predictions_neg)
	pos_results = Counter(final_predictions_pos)

	true_neg = neg_results['Negative']
	true_pos = pos_results['Positive']

	neg_correct = true_neg / len(final_predictions_neg)
	pos_correct = true_pos / len(final_predictions_pos)

	print 'Results:\n'
	print 'Out of Negative Test reviews, the Classifier predicited ', neg_correct, ' percent correct.\n'
	print 'Out of Positive Test reviews, the Classifier predicited ', pos_correct, ' percent correct.\n'


# ********** FOR LARGE TESTS ************

with open("neg_large.csv") as file:
	r_neg = list(csv.reader(file))

with open("pos_large.csv") as file:
	r_pos = list(csv.reader(file)) 	

reviews_neg = r_neg
reviews_pos = r_pos

#SMALL FILES ARE NOW USED FOR TESTING.
with open("neg.csv") as file:
	reviews_neg_test = list(csv.reader(file))

with open("pos.csv") as file:
	reviews_pos_test = list(csv.reader(file))


# ********* FOR SMALL TESTS ****************
#with open("neg.csv") as file:
#	r_neg = list(csv.reader(file))

#with open("pos.csv") as file:
#	r_pos = list(csv.reader(file)) 	

#reviews_neg = r_neg[:5000]
#reviews_pos = r_pos[:5000]


#reviews_neg_test = r_neg[5000:]
#split the positive reviews into train data and test data
#reviews_pos_test = r_pos[5000:]
#split the negative reviews into train data and test data



#remove punctuation and get counts for negative text.		
#TRAINING DATA NEG
remove_punc(reviews_neg)
neg_text = get_text(reviews_neg)
counter_neg = get_counts(neg_text)


#remove punctuation and get counts for positive text.
#TRAINING DATA POS
remove_punc(reviews_pos)
pos_text = get_text(reviews_pos)
counter_pos = get_counts(pos_text)


pos_common = dict(counter_pos.most_common(10))
neg_common = dict(counter_neg.most_common(10))



#Number of unique words in positive class, and unique class
unique_pos = len(counter_pos)
unique_neg = len(counter_neg)
total_word_count = unique_pos+unique_neg

#get number of positive and neg reviews
num_neg_reviews = len(reviews_neg)
num_pos_reviews = len(reviews_pos)

#probabilities of class 
prob_class_pos = num_pos_reviews / (num_pos_reviews + num_neg_reviews)
prob_class_neg = num_neg_reviews / (num_pos_reviews + num_neg_reviews)

feat_prob_pos, feat_prob_neg = train(total_word_count, unique_pos, unique_neg, counter_pos, counter_neg)


# ***************** TRAINING DONE  ***************************

# UNCOMMENT THE BELOW LINE TO RUN TEST DATA ON NEG.CSV AND POS.CSV
test_data()
print "\nThis program is a Naive Bayes Classifier for predicting sentiment in movie reviews."
print "\nIt is trained using over 70,000 Movie reviews."
print "\nEnter text input and the classifier will make a prediction on whether the review is positive, or negative."
print "\nPrint exit to quit the program."




while True:
	
	review = raw_input("\nPlease enter a movie review: ")

	if (review == "exit"):
		sys.exit()

	review = review.lower()	
	review = review.split()
	predict_neg = make_class_prediction(review, unique_neg, prob_class_neg, feat_prob_neg, num_neg_reviews, neg_common)
	predict_pos = make_class_prediction(review, unique_pos, prob_class_pos, feat_prob_pos, num_pos_reviews, pos_common)
	print "\n Negative Prediction Probability: ", predict_neg
	print "\n Positive Prediction Probability: ", predict_pos
		
	if (predict_neg > predict_pos):
			print "\nYour review was predicited as a negative review."
	else:
			print "\nYour review was predicted as a positive review."

	print "\n\n\n\n\n"		