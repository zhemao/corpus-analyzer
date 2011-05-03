from __future__ import division
import csv, re, os
from settings import STATIC_PATH
from datetime import date

def countwords(text, words):
	"""Counts all of the words in text. A word is defined as a group of alphanumeric
	characters, hyphens, or underscores. The word counts are added to the dictionary
	words and the total number of words counted is returned"""
	#the regular expression for a word
	p = re.compile(r'[\w\d\-]+\b')
	#the total number of words
	total = 0
	#use finditer instead of findall to avoid using up a lot of memory
	for m in p.finditer(text):
		#we want this to be case-insensitive
		s = m.group().lower()
		# store the word only if it is greater than 3 characters long
		if len(s)>2:
			#if the word is already in our dictionary, increment the existing value
			if s in words:
				words[s]+=1
			#otherwise, create a new key and set its value equal to 1
			else: words[s]=1
		#increment total
		total+=1
	return total

def genwordcount(inf):
	"""Handle a single file, this file should be a plaintext file with
	extension .txt"""
	#initialize words and total
	words = {}
	total = 0
	#open the text file and then count the words line-by-line
	for line in inf.file.readlines():
		total+=countwords(line, words)
	#reverse the words and their counts and then sort from most to least used
	reverse = [(num,word) for word,num in words.items()]
	reverse.sort(reverse=True)
	#flip everything back
	final = [('TOTAL',total)]+[(word,num,'%1.4f%%' % (num/total*100)) for num,word in reverse]
	#write to file
	return store(inf,final)
	
def store(inf, words):
	datadir = 'files/data/'+date.today().strftime('%Y/%m/%d/')
	if not os.path.exists(STATIC_PATH+datadir):
		os.makedirs(STATIC_PATH+datadir)
	dataname = datadir+inf.filename[:-3]+'csv'
	data = open(STATIC_PATH+dataname, 'w')
	out = csv.writer(data)
	out.writerows(words)
	data.close()
	return dataname

