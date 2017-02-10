# -*- coding: utf-8 -*-  
#import urllib2
#import urllib
from mongodb_queue import MogoQueue
from Download import request
from bs4 import BeautifulSoup

'''
def getHtml():
	page = urllib.urlopen("http://www.chinalawedu.com/falvfagui/")
	html = page.read()
	reg=r'class="fenlei_txt"'
	soup=BeautifulSoup(html,"lxml")
'''

law_queue=MogoQueue('falvfagui', 'title_queue')
def start(url):
	response = request.get(url,3)
	soup=BeautifulSoup(response.text,'html.parser')
	#print soup.prettify().encode('utf-8')
	all_div = soup.find_all('div', class_="fenlei_txt")
	
	#law_queue.push('lianjie','ok')
	
	for div in all_div:
		#print div.prettify()
		all_a = div.find_all('a')
		for a in all_a:
			title = a.get_text()
			url = a['href']
			law_queue.push(url, title)  #将待爬取网页和标题写入队列
		
		
	
if __name__ == "__main__":
	start("http://www.chinalawedu.com/falvfagui/")