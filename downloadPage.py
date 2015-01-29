import threading
import logging
import time
from question import Question

logging.basicConfig(level = logging.DEBUG,format='(%(threadName)-10s) %(message)s',) 

class DownloadThread(threading.Thread):

    def __init__(self, threadingSum, url):
        threading.Thread.__init__(self)
        self.url = url
        self.threadingSum = threadingSum

    def run(self):
        with self.threadingSum:
            logging.debug("%s start" % self.url)
            question = Question(self.url)
            title = question.get_title()
            detail = question.get_detail()
            answerNum = question.get_answer_num()
            followersNum = question.get_followers_num()
            print title, detail, answerNum, followersNum
            logging.debug("%s done" % self.url)
