#!/usr/bin/env python

from __future__ import division
import web, csv, settings, json
from settings import STATIC_PATH, STATIC_URL, TEMPLATE_PATH
from counter import genwordcount
from models import Corpus
from search import search_user_corpus
from web.session import DiskStore, Session
from web.contrib.template import render_jinja

web.config.debug = False
render = render_jinja('templates', 'utf-8')

urls = (
	'/api/', 'API',
	'/', 'Index',
	'/upload/', 'Upload',
	'/error/', 'Error',
	'/nocookie/', 'Nocookie',
	'/results/','Results',
	'/compare/','Compare',
)

app = web.application(urls, locals())

session = Session(app, DiskStore("sessions"))

class Index:
	def GET(self):
		session.test = "testcookie";
		return render.index()

class Upload:
	def GET(self):
		if session.get('test')!='testcookie':
			raise web.seeother('/nocookie/')
		return render.post_file()
	def POST(self):
		textfile = web.input(text={}).text
		if textfile.type == 'text/plain' and textfile.filename[-3:]=='txt':
			session.data = genwordcount(textfile)
			raise web.seeother('/results/')
		raise web.seeother('/error/')

class Results:
	def GET(self):
		if not session.get('data'):
			raise web.seeother('/')
		rdr = csv.reader(open(STATIC_PATH+session['data'], 'r'))
		results = []
		total = 0
		for row in rdr:
			web.debug(row)
			if rdr.line_num==102: break
			if rdr.line_num==1: total = int(row[1])
			elif rdr.line_num>51: results[rdr.line_num-52]+=row
			else: results.append(row)
		return render.results(total=total,results=results,
							csvpath=STATIC_URL+session['data'])
	
class Nocookie:
	def GET(self):
		return render.nocookie()

class Error:
	def GET(self):
		return render.error()

class Compare:
	def GET(self):
		if not web.input().get('word'):
			err_mess = '<html><head><title>No Input Value</title></head>'
			err_mess+='<body>You must provide the word to be searched.</body></html>'
			return err_mess
		word = web.input().word
		table = []
		for name in Corpus.names:
			corpus = Corpus.load_corpus(name)
			count, relfreq = corpus.find_word(word)
			tup = (corpus.fullname, count, '%1.4f%%' % (relfreq*100))
			table.append(tup)
		if session.get('data'):
			f = open(STATIC_PATH+session['data'])
			count, relfreq = search_user_corpus(f, word)
			tup = ("Your Writing", count, '%1.4f%%' % (relfreq*100))
			table.append(tup)
		return render.comparison(word=word, table=table)

class API:
	def GET(self):
		web.header('Content-type','application/json')
		if not web.input().get('q'):
			return json.dumps({'ok':False, 'mess':'no query given'})
		try:
			q = json.loads(web.input().q)
		except ValueError:
			return json.dumps({'ok':False, 'mess':'could not parse json'})
		if isinstance(q, dict):
			return json.dumps(self._get_json_resp(**q))
		else:
			resp = []
			for row in q:
				resp.append(self._get_json_resp(**row))
			return json.dumps(resp)
		
	def _get_json_resp(self, corpus=None, word=None):
		corpusname = corpus
		if not corpusname or not word:
			return {'ok':False, 'mess':'bad query'}
		corpus = Corpus.load_corpus(corpusname)
		count, relfreq = corpus.find_word(word)
		return {'ok':True, 'count':count, 'relfreq':relfreq}

if __name__ == '__main__':
	app.run()
