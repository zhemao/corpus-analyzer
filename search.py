from __future__ import division
import csv

def search_user_corpus(f, search):
	search = str(search).lower()
	rdr = csv.reader(f)
	count = 0
	total = 0
	for row in rdr:
		if row[0]=='TOTAL':
			total = int(row[1])
			continue
		if row[0]==search:
			count = int(row[1])
			break
	return count, count/total
	

