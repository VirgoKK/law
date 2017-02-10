# -*- coding:utf-8 -*-
import os
import time
import threading
import multiprocessing
from mongodb_queue import MogoQueue
from Download import request
from bs4 import BeautifulSoup

SLEEP_TIME=1

def law_crawler(max_threads=10):
	tit_queue = MogoQueue('falvfagui', 'title_queue') #获取的标题，url的队列
	def pageurl_crawler():
		while True:
			try:
				url = tit_queue.pop()
				print(url)
			except KeyError:
				print('队列没有数据')
				break
		else:
			req = request.get(url, 3).text
			title = tit_queue.pop_title(url)
			path = str(title).encode('utf-8')
			mkdir(path)
			os.chdir('D:\law\\' + path)

	def mkdir(path):
		#path = path.strip()
		isExists = os.path.exists(os.path.join("D:\law", path))
		if not isExists:
			print('新建文件夹')
			osmakedirs(os.path.join("D:\law", path))
			return True
		else:
			print('文件夹已经存在')
			return False
		
	threads = []
	while threads or tit_queue:
		"""
		这儿tit_queue用上了，就是我们__bool__函数的作用，为真则代表我们MongoDB队列里面还有数据
		threads 或者 crawl_queue为真都代表我们还没下载完成，程序就会继续执行
		"""
		for thread in threads:
			if not thread.is_alive(): ##is_alive是判断是否为空,不是空则在队列中删掉
				threads.remove(thread)
		while len(threads) < max_threads or tit_queue.peek(): ##线程池中的线程少于max_threads 或者 tit_qeue时
			thread = threading.Thread(target=pageurl_crawler) ##创建线程
			thread.setDaemon(True) ##设置守护线程
			thread.start() ##启动线程
			threads.append(thread) ##添加进线程队列
		time.sleep(SLEEP_TIME)
		
def process_crawler():
    process = []
    num_cpus = multiprocessing.cpu_count()
    print(('将会启动进程数为：'), num_cpus)
    for i in range(num_cpus):
        p = multiprocessing.Process(target=law_crawler)
        p.start() 
        process.append(p) 
    for p in process:
        p.join() 
		
if __name__ == "__main__":
	process_crawler()