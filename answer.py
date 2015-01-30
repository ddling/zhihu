# _*_ coding: utf-8 _*_

from session import Session

from bs4 import BeautifulSoup as bs
import requests
import os
from utils import Utils

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

        vote = self.soup.find_all("span", class_ = "count")[0].string

        return vote

    def get_answer_content(self):

        noscript = self.soup.find_all("noscript")

        for one in noscript:
            one.decompose()

        content_image = self.soup.find_all("img", class_ = "content_image")

        for one in content_image:
            one.decompose()

        img_content = self.soup.find_all("div", class_ = "zm-item-answer")
        for pic in img_content:
            pic_urls = pic.find_all("img", class_ = "origin_image")
            for url in pic_urls:
                img_name = url["data-actualsrc"].split("/")[-1]
                url["src"] = "images/" + img_name

        answer = self.soup.find_all("div", class_ = "zm-editable-content")[2]

        return answer

    def get_all_pics(self):

        urls = []
        count = 0
        pics = self.soup.find_all("div", class_ = "zm-item-answer")
        for pic in pics:
            pic_urls = pic.find_all("img")
            for url in pic_urls:
                print url
                if count % 2 == 0 and url["src"].split("/")[0] == 'http:':
                    urls.append(url["src"])
        return urls[1:]

if __name__ == "__main__":
    answer = Answer("http://www.zhihu.com/question/27463075/answer/38414209")
    author = answer.get_author()
    print author
    votes = answer.get_votes()
    print votes
    all_pics = answer.get_all_pics()
    for url in all_pics:
        print url
    answer.get_answer_content()
    # print answer_
