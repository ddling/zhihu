# _*_ coding: utf-8 _*_

import threading
import logging
import requests
import os

from dbHandler import DbHandler
from answer import Answer
from question import Question

logging.basicConfig(level = logging.DEBUG,format='(%(threadName)-10s) %(message)s',) 

class DownloadImg(threading.Thread):

    def __init__(self, threadingSum, url):
        threading.Thread.__init__(self)
        self.dbHandler = DbHandler()
        self.url = url
        self.threadingSum = threadingSum

    def run(self):
        with self.threadingSum:
            logging.debug("%s start!" % self.url) 
            pic_name = self.url.split("/")[-1]
            request = requests.get(self.url, stream = True, timeout=10)
            with open(os.getcwd() + "/tmp/html/images/" + pic_name, 'wb') as fd:
                for chunk in request.iter_content():
                    fd.write(chunk)
            logging.debug("%s done!" % self.url) 

if __name__ == '__main__':
    #设置线程数 
    threadingSum = threading.Semaphore(20)

    dbHandler = DbHandler()

    question = Question("http://www.zhihu.com/question/26702926")

    answer = Answer("http://www.zhihu.com/question/26702926/answer/33843851")
    img_urls =  answer.get_all_pics()

    for url in img_urls:
        t = DownloadImg(threadingSum, url)
        t.start()

    for t in threading.enumerate(): 
        if t is threading.currentThread(): 
            continue
        t.join()
