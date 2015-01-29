# _*_ coding: utf-8 _*_

from session import Session

from bs4 import BeautifulSoup as bs
import requests
import os

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Answer:

    def __init__(self, url):
        self.url        = url
        s               = Session()
        self.session    = s.get_session()
        self.initSoup()

    def initSoup(self):
        request = self.session.get(self.url)
        self.soup = bs(request.content)

    def get_author(self):

        author = None
        if self.soup.find_all("h3", class_ = "zm-item-answer-author-wrap")[0].string == u"匿名用户":
            author = "匿名用户"
        else:
            author = self.soup.find_all("h3", class_ = "zm-item-answer-author-wrap")[0].find_all("a")[1].string

        return author

    def get_votes(self):

        vote = int(self.soup.find_all("span", class_ = "count")[0].string)

        return vote

    def get_answer_content(self):

        answer = self.soup.find_all("div", class_ = "zm-editable-content")[0]

        return answer

if __name__ == "__main__":
    answer = Answer("http://www.zhihu.com/question/20357990/answer/38277514")
    author = answer.get_author()
    print author
    votes = answer.get_votes()
    print votes
    answer_ = answer.get_answer_content()
    print answer_
