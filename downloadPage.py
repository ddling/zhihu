# _*_ coding: utf-8

import threading
import logging
import time
from question import Question
from answer import Answer
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
                # 插入新的问题
                question = Question(self.url)
                title = question.get_title()
                detail = question.get_detail()
                answerNum = question.get_answer_num()
                followersNum = question.get_followers_num()
                tags = ""
                for tag in question.get_tags():
                    tags += tag + ";"
                tags = tags[0: len(tags) - 1]
                questionDict = {"url": self.url, "title": title, 
                                "detail": detail, "followers": followersNum, 
                                "answerNum": answerNum, "tags": tags}
                dbHandler.insertNewQuestion(questionDict)

                zh_qid = dbHandler.getAnsIdByUrl(self.url)
                # 插入新的答案
                for answer_link in question.get_all_answer_link():
                    answer = Answer(answer_link)
                    author = answer.get_author()
                    votes = answer.get_votes()
                    contents = answer.get_answer_content()
                    answer = {"url": answer_link, "author": author, "zh_qid": zh_qid, 
                              "votes": votes, "contents": contents}
                    dbHandler.insertNewAnswer(answer)

                dbHandler.close()

            logging.debug("%s done" % self.url)
