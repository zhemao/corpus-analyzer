from __future__ import division
from settings import STATIC_PATH
import csv

fullnames = {'anc':'American National Corpus', 'bnc': 'British National Corpus'}

class Corpus(object):
	def __init__(self, abbrev, fullname, total, words):
		self.abbrev = abbrev
		self.fullname = fullname
		self.total = total
		self.words = words
	
	@classmethod
	def load_corpus(cls, abbrev):
		fullname = fullnames[abbrev]
		words = {}
		total = 0
		with open(STATIC_PATH+'files/corpora/'+abbrev+'-count-o5.csv') as f:
			rdr = csv.reader(f)
			for word, count in rdr:
				count = int(count)
				if word=='TOTAL': total = count
				if word in words:
					words[word] += count
				else: words[word] = count
		if fullname and total:
			return Corpus(abbrev, fullname, total, words)
		return None
		
	def find_word(self, word):
		count = self.words.get(word, 0)
		if self.total:
			return count, float(count/self.total)
		return 0, 0.0
	
	def add_word(self, word, count):
		self.total+=count
		if word in self.words:
			self.words[word]+=count
		else: self.words[word] = count
	
	names = ('anc','bnc')
