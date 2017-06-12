# NLP-Bayes
Natural Language Processing Naive Bayes Classifier for predicting sentiment in movie reviews


Remarks (June 12, 2017):

There are two sets of training data, small: neg.csv, pos.csv and large: neg_large.csv, pos_large.csv
The small datasets contain 5331 reviews in neg.csv, and 5331 reviews in pos.csv
Originally, 5000 from each .csv file were used to train the model, and the remaining 331 reviews used to test accuracy of the Classifier.

When using the small file, I noticed that perhaps there wasn't enough data for the data to computer predictions accurately.
For example, when given a review "This was a good movie" the machine predicted this was a negative review.

After using the large file I noticed that user input was predicted correct more often.
However, when I used the small files as test data for the classifer, it predicited positive correct very often, 
but predicited negative badly.

This may also be because the large datasets are not the same size. (approx. 41,000 Positive Reviews, 33,000 Negative Reviews).
Because we use the # of reviews in each class for calculations this may skewer the results a bit.

I'll be doing more testing next week when I have some time.

Currently the classifier is setup to take user input reviews after the model has been trained. The function test_data() has been commented 
out for now.

Noticing that common words have a very large discrepancy in how many times they may appear in a review class: (ie, the appears over 20,000 times in negative
reviews, but the appears only 14,000 times in positive reviews).