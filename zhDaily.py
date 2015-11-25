# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup

URL = 'http://daily.zhihu.com'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)

def listByDelimeter(ls, delimeter):
    if len(ls)%delimeter != 0:
        return ls
    parts = len(ls)/delimeter
    result = []
    for i in xrange(delimeter):
        for j in xrange(parts):
            result.append(ls[i + j*delimeter])
    return result

class Main(Wox):
  
    def request(self,url):
	#get system proxy if exists
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
	    proxies = {
		"http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
		"https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
	    }
	    return requests.get(url,proxies = proxies)
	return requests.get(url)
			
    def query(self, param):
	r = self.request(URL)
	bs = BeautifulSoup(r.content, 'html.parser')
	posts = bs.find_all('div', 'box')
        newPosts = listByDelimeter(posts, 10)
	result = []
	for p in newPosts:

            if p.find('a') is None:
                continue
            
            title = p.find('span', 'title').text
            link = URL + p.find("a")['href']
            
            item = {
                'Title': full2half(title),
                'SubTitle': u'enter to open',
                'IcoPath': os.path.join('img', 'zhd.png'),
                'JsonRPCAction': {
                    'method': 'open_url',
                    'parameters': [link]
                }
            }
            result.append(item)
        
	return result
    
    def open_url(self, url):
	webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)

if __name__ == '__main__':
    Main()
