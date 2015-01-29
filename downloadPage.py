import threading
import logging
import time
from question import Question
from dbHandler import DbHandler

logging.basicConfig(level = logging.DEBUG,format='(%(threadName)-10s) %(message)s',) 

class DownloadThread(threading.Thread):

    def __init__(self, threadingSum, url):
        threading.Thread.__init__(self)
        self.url = url
        self.threadingSum = threadingSum

    def run(self):
        with self.threadingSum:
            logging.debug("%s start" % self.url)
            dbHandler = DbHandler()
            if not dbHandler.hasQuestion(self.url):
                question = Question(self.url)
                title = question.get_title()
                detail = question.get_detail()
                answerNum = question.get_answer_num()
                followersNum = question.get_followers_num()
                questionDict = {"url": self.url, "title": title, "detail": detail, "followers": followersNum, "answerNum": answerNum}
                dbHandler.insertNewQuestion(questionDict)
                dbHandler.close()
            logging.debug("%s done" % self.url)
