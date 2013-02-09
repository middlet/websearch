#!/usr/bin/env python

import config ### replace this with a file containing your accountkey
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
	sterms = terms.replace(' ', '+')
	bing_url = 'http://www.bing.com/news/search'
	search_url = '%s?q=%s' % (bing_url, sterms)
	# get the data
	res = requests.get(search_url)
	data = res.content
	url_list = []
	for ri in pat.finditer(data):
		s,e = ri.end()+1, data.find('"', ri.end()+1)
		url_list.append(data[s:e])
	#
	return url_list
	

if __name__ =='__main__':
	term = 'today'
	ul1 = search_bing_api(term)
	ul2 = search_bing_web(term)
	
	
	
