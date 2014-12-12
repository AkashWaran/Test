import nltk, re
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

threshold = 0.6

class Chain():
    def __init__(self, words, senses):
	self.words = set(words)
	self.senses = set(senses)

    def addWord(self, word):
	self.words.add(word)

    def addSense(self, sense):
	self.senses.add(sense)

    def getWords(self):
	return self.words

    def getSenses(self):
	return self.getSenses

lexical_chains = []

def add_word(word):
    for chain in lexical_chains:
	for synset in wn.synsets(word):
	    for sense in chain.senses:
		if sense.wup_similarity(synset) >= threshold:
		    chain.addWord(word)
		    chain.addSense(synset)
		    return
    lexical_chains.append(Chain([word], wn.synsets(word)))

def print_chains():
    for chain in lexical_chains:
	print ", ".join(str(e) for e in chain.getWords())

text = "If a banana's skin shows dark brown or black spots, these are most likely sunburn spots and not necessarily a sign of over ripeness or rotting. If bananas suffer very long exposure to ultraviolet radiation during their growing period, they develop a tan in their own unique splotchy way."

tokens = nltk.word_tokenize(text)
tokens = [w.lower() for w in tokens]

stopwords = nltk.corpus.stopwords.words('english')

for w in tokens:
    if w not in stopwords and re.match("^[a-z][a-z]+$", w) :
	add_word(w)

print_chains()
