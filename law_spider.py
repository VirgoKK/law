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
	tit_queue = MogoQueue('falvfagui', 'title_queue') #��ȡ�ı��⣬url�Ķ���
	def pageurl_crawler():
		while True:
			try:
				url = tit_queue.pop()
				print(url)
			except KeyError:
				print('����û������')
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
			print('�½��ļ���')
			osmakedirs(os.path.join("D:\law", path))
			return True
		else:
			print('�ļ����Ѿ�����')
			return False
		
	threads = []
	while threads or tit_queue:
		"""
		���tit_queue�����ˣ���������__bool__���������ã�Ϊ�����������MongoDB�������滹������
		threads ���� crawl_queueΪ�涼�������ǻ�û������ɣ�����ͻ����ִ��
		"""
		for thread in threads:
			if not thread.is_alive(): ##is_alive���ж��Ƿ�Ϊ��,���ǿ����ڶ�����ɾ��
				threads.remove(thread)
		while len(threads) < max_threads or tit_queue.peek(): ##�̳߳��е��߳�����max_threads ���� tit_qeueʱ
			thread = threading.Thread(target=pageurl_crawler) ##�����߳�
			thread.setDaemon(True) ##�����ػ��߳�
			thread.start() ##�����߳�
			threads.append(thread) ##��ӽ��̶߳���
		time.sleep(SLEEP_TIME)
		
def process_crawler():
    process = []
    num_cpus = multiprocessing.cpu_count()
    print(('��������������Ϊ��'), num_cpus)
    for i in range(num_cpus):
        p = multiprocessing.Process(target=law_crawler)
        p.start() 
        process.append(p) 
    for p in process:
        p.join() 
		
if __name__ == "__main__":
	process_crawler()