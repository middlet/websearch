#!/usr/bin/env python

import config ### replace this with a file containing your accountkey
import random
import re
import requests
import sys
import time

from BeautifulSoup import BeautifulSoup

pat = re.compile('<div class="newstitle"><a href=')

def time_it(func):
	def wrapper(*arg, **kw):
		t0 = time.time()
		res = func(*arg, **kw)
		t1 = time.time()
		print >> sys.stderr, '{:<20}\t{:>15}'.format(func.func_name, t1-t0)
		return res
	return wrapper

@time_it
def search_bing_api(terms):
	"""
	search bing using the azure api
	"""
	bing_url = 'https://api.datamarket.azure.com/Bing/Search/v1/News'
	search_url = '%s?$format=json&$top=10' % bing_url
	res = requests.post(search_url, params={'Query':"'%s'"%terms},
		auth=(config.accountkey, config.accountkey))
	j = res.json()
	url_list = []
	for ri in j['d']['results']:
		url_list.append(ri['Url'])
	#
	return url_list
	
@time_it
def search_bing_web(terms):
	"""
	search bing using a screen scrape
	
	probably should change the content header so we dont look like a bot
	"""
	user_agents = [
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
		'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
		'Mozilla/5.0 (compatible; Konqueror/4.3; Linux 2.6.31-16-generic; X11) KHTML/4.3.2 (like Gecko)',
		'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',
		'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',
		'Mozilla/5.0 (X11; U; Linux x86_64; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/531.2+',
		]
	
	sterms = terms.replace(' ', '+')
	bing_url = 'http://www.bing.com/news/search'
	search_url = '%s?q=%s' % (bing_url, sterms)
	# get the data
	#headers = {}
	#headers['User-Agent'] = random.choice(user_agents)
	res = requests.get(search_url)#, headers=headers)
	data = res.content
	url_list = []
	for ri in pat.finditer(data):
		s,e = ri.end()+1, data.find('"', ri.end()+1)
		url_list.append(data[s:e])
	#
	return url_list
	

if __name__ =='__main__':
	term = 'today'
	for i in range(10):
		ul1 = search_bing_api(term)
		ul2 = search_bing_web(term)
		print len(ul1), len(ul2)
	
	
	
