import nltk 
from nltk.corpus import movie_reviews 
import random

documents = [(list(movie_reviews.words(fileid)), category)
    for category in movie_reviews.categories()
	for fileid in movie_reviews.fileids(category)]

#random.shuffle(documents)

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = all_words.keys()[:2000] 

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
	features['contains(%s)' % word] = (word in document_words)
    return features 

#featuresets = [(document_features(d), c) for (d,c) in documents]

#train_set, test_set = featuresets[100:], featuresets[:100]
#classifier = nltk.NaiveBayesClassifier.train(train_set)
#print nltk.classify.accuracy(classifier, test_set)

def readSubjectivity(path):
    flexicon = open(path, 'r')
    # initialize an empty dictionary
    sldict = { }
    for line in flexicon:
	fields = line.split()   # default is to split on whitespace
	# split each field on the '=' and keep the second part as the value
	strength = fields[0].split("=")[1]
	word = fields[2].split("=")[1]
	posTag = fields[3].split("=")[1]
	stemmed = fields[4].split("=")[1]
	polarity = fields[5].split("=")[1]
	if (stemmed == 'y'):
	    isStemmed = True
	else:
	    isStemmed = False
	# put a dictionary entry with the word as the keyword and a list of the other values
	sldict[word] = [strength, posTag, isStemmed, polarity]
    return sldict
															    
SLpath = "./Dictionary/subjclueslen1-HLTEMNLP05.tff"
SL = readSubjectivity(SLpath)

#print "Using custom dictionary based featureset"

def get_polarity_val(strength, polarity): 
    if strength == 'weaksubj' and polarity == 'positive':
	return 1
    if strength == 'strongsubj' and polarity == 'positive':
	return 2
    if strength == 'weaksubj' and polarity == 'negative':
	return -1
    if strength == 'strongsubj' and polarity == 'negative':
	return -2
    else :
	return 0

def custom_features(document, SL):
    document_words = set(document) 
    features = {} 
    for word in word_features: 
	features['contains(%s)' % word] = (word in document_words) 
    pol = 0
    flag = 0
    for word in document_words:
	if word in SL:
	    strength, posTag, isStemmed, polarity = SL[word]
	    pol_val = get_polarity_val(strength, polarity)
	    if flag == 0 :
		if pol_val < 0 :
		    flag = -1
		elif pol_val > 0 :
		    flag = 1
	    else :
		if pol_val == 0:
		    pol += flag
		else :
		    pol += (flag * pol_val)
		flag = 0
	else :
	    pol += flag
	    flag = 0
    if pol > 0 :
	features['polarity'] = 'positive'
    elif pol < 0 :
	features['polarity'] = 'negative'
    return features

#custom_featuresets = [(custom_features(d, SL), c) for (d,c) in documents]

#train_set, test_set = custom_featuresets[100:], custom_featuresets[:100]
#classifier = nltk.NaiveBayesClassifier.train(train_set)
#print nltk.classify.accuracy(classifier, test_set)

def custom2_features(document, SL):
    document_words = set(document) 
    features = {} 
    for word in word_features: 
	features['contains(%s)' % word] = (word in document_words) 
    pol = 0
    for word in document_words:
	if word in SL:
	    strength, posTag, isStemmed, polarity = SL[word]
	    if polarity == 'negative' :
		pol += -1
	    elif polarity == 'positive' :
		pol += 1
    if pol > 0:
	features['polarity'] = 'positive'
    elif pol < 0:
	features['polarity'] = 'negative'
    return features

#custom2_featuresets = [(custom2_features(d, SL), c) for (d,c) in documents]

#train_set, test_set = custom2_featuresets[100:], custom2_featuresets[:100]
#classifier = nltk.NaiveBayesClassifier.train(train_set)
#print nltk.classify.accuracy(classifier, test_set)


number_of_runs = 10
basecase_val = 0
customcase_val = 0
normalsum_val = 0

for i in range(0, number_of_runs):
    random.shuffle(documents)

    #running basecase
    featuresets = [(document_features(d), c) for (d,c) in documents]

    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    basecase_val += nltk.classify.accuracy(classifier, test_set)

    #running customcase
    custom_featuresets = [(custom_features(d, SL), c) for (d,c) in documents]

    train_set, test_set = custom_featuresets[100:], custom_featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    customcase_val += nltk.classify.accuracy(classifier, test_set)

print "basecase accurace"
print (basecase_val / number_of_runs)
print "Using custom dictionary based featureset accuracy"
print (customcase_val / number_of_runs)
