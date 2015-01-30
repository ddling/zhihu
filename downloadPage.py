# _*_ coding: utf-8

import threading
import logging
import time
import os

from question import Question
from answer import Answer
from dbHandler import DbHandler
from utils import Utils

logging.basicConfig(level = logging.DEBUG,format='(%(threadName)-10s) %(message)s',) 

class DownloadThread(threading.Thread):

    def __init__(self, threadingSum, url):
        threading.Thread.__init__(self)
        self.url = url
        self.threadingSum = threadingSum

    def storeTheAnswer(self, zh_aid, contents):

        utils = Utils()
        tmp_answer_content_dir = utils.get("tmp_answer_content_dir")
        with open(os.getcwd() + "/" + tmp_answer_content_dir + "/%d.txt" % (zh_aid) , 'w') as fb:
            fb.write(str(contents))

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

                zh_qid = dbHandler.getQueIdByUrl(self.url)
                # 插入新的答案
                for answer_link in question.get_all_answer_link():

                    answer = Answer(answer_link)
                    author = answer.get_author()
                    votes = answer.get_votes()
                    answerDict = {"url": answer_link, "author": author, "zh_qid": zh_qid, 
                              "votes": votes}
                    dbHandler.insertNewAnswer(answerDict)

                    # 插入图片地址
                    zh_aid = dbHandler.getAnsIdByUrl(answer_link)

                    for imgUrl in answer.get_all_pics():
                        dbHandler.insertNewImgUrl(zh_aid, imgUrl)

                    contents = answer.get_answer_content()
                    self.storeTheAnswer(zh_aid, contents)

                dbHandler.close()

            logging.debug("%s done" % self.url)
