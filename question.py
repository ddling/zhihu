# _*_ coding: utf-8 _*_

from session import Session

from bs4 import BeautifulSoup as bs
import requests
import os

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Question:

    def __init__(self, url):

        if self.isValidQuestionUrl(url):
            self.url = url
        else:
            raise ValueError("The question url '%s' is not valid" % (url))
            return
        s = Session()
        self.session = s.get_session()
        self.initSoup()

    def initSoup(self):

        request = self.session.get(self.url)
        self.soup = bs(request.content)

    def isValidQuestionUrl(self, url):
        if url[0: len(url) - 8] != "http://www.zhihu.com/question/":
            return False
        else:
            return True

    def get_title(self):

        title = self.soup.find("h2", class_ = "zm-item-title").string.replace("\n", "").encode("utf-8")
        return title

    def get_detail(self):

        detail = self.soup.find("div", id = "zh-question-detail").div.get_text().encode("utf-8")
        return detail

    def get_answer_num(self):

        answer_num = 0
        answer_num = int(self.soup.find("h3", id = "zh-question-answer-num")["data-num"])
        return answer_num

    def get_followers_num(self):

        followers_num = 0
        followers_num = int(self.soup.find("div", class_ = "zg-gray-normal").a.strong.string)
        return followers_num

    def get_tags(self):

        tags = []
        tagList = self.soup.find_all("a", class_ = "zm-item-tag")
        for oneTag in tagList:
            tag = oneTag.contents[0].encode("utf-8").replace("\n", "")
            tags.append(tag)

        return tags

    def get_all_answer_link(self):

        answer_links = []
        for j in range(min(10, self.get_answer_num())):
            answer_link = "http://www.zhihu.com" + self.soup.find_all("a", class_ = "answer-date-link")[j]["href"]
            print answer_link
            answer_links.append(answer_link)

        return answer_links

    def download_all_pics(self, urls):

        for url in urls:
            pic_name = url.split("/")[-1]
            request = requests.get(url, stream = True)
            with open(os.getcwd() + "/" + pic_name, 'wb') as fd:
                for chunk in request.iter_content():
                    fd.write(chunk)

