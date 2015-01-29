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
            raise ValueError("The question url is not valid")
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

    def get_all_authors(self):
        
        authors = []
        for j in range(min(self.get_answer_num(), 50)):
            author = None
            if self.soup.find_all("h3", class_ = "zm-item-answer-author-wrap")[j].string == u"匿名用户":
                author = "匿名用户"
            else:
                author = self.soup.find_all("h3", class_ = "zm-item-answer-author-wrap")[j].find_all("a")[1].string
            authors.append(author)

        return authors

    def get_all_votes(self):

        votes = []
        for j in range(min(self.get_answer_num(), 50)):
            vote = self.soup.find_all("span", class_ = "count")[j].string
            votes.append(vote)

        return votes

    def get_all_answers(self):

        answers = []
        for j in range(min(self.get_answer_num(), 50)):
            answer = self.soup.find_all("div", class_ = "zm-editable-content")[j]
            answers.append(answer)

        return answers

    def get_all_pics(self):

        urls = []
        count = 0
        pics = self.soup.find_all("div", class_ = "zm-editable-content")  
        for pic in pics:
            pic_urls = pic.find_all("img")
            for url in pic_urls:
                if count % 2 == 0:
                    urls.append(url["src"])
                count += 1
        return urls

    def download_all_pics(self, urls):

        for url in urls:
            pic_name = url.split("/")[-1]
            request = requests.get(url, stream = True)
            with open(os.getcwd() + "/" + pic_name, 'wb') as fd:
                for chunk in request.iter_content():
                    fd.write(chunk)

