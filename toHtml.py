# _*_ coding: utf-8 _*_

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import os
import threading

from dbHandler import DbHandler
from utils import Utils

from downloadImg import DownloadImg
from bs4 import BeautifulSoup as bs

class ToHtml:

    def __init__(self):
        self.dbHandler = DbHandler()

    def createHtml(self):

        html_tpl = u'''<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="provider" content="www.cnepub.com"/>
        <meta name="builder" content="epubBuilder present by www.cnepub.com"/>
        <meta name="right" content="该文档由epubBuilder生成。epubBuilder为掌上书苑（www.cnepub.com)提供的epub制作工具，仅供个人交流与学习使用。在未获得掌上书苑的商业授权前，不得用于任何商业用途。"/>
        <link rel="stylesheet" type="text/css" href="css/main.css"/>
        <title>%(title)s</title>
        </head>
        <body>
        <center>
            <h3>%(title)s</h3>
        </center>
        <hr>
        <div class="band">
            %(band)s
        </div>
        <div class="answer-content">
            %(content)s
        </div>
        </body>
        '''

        questions = self.dbHandler.getQuestions()
        utils     = Utils()

        for question in questions:
            zh_qid    = question["zh_qid"]
            q_url     = question["url"]
            title     = question["title"]
            detail    = question["detail"]
            tags      = question["tags"]
            followers = question["followers"]
            answerNum = question["answerNum"]

            band = ""
            
            band += '<div class = "tags">\n'
            for tag in tags.split(";"):
                band += '<span>' + tag + '</span>\n'
            band += '</div>\n'
            band += '<div class = "info"><span><strong>%d</strong>个回答</span><span><strong>%d</strong>人关注该问题</span></div>\n' % (answerNum, followers)
            band += '<div class = "detail">' + detail + '</div>\n'
            band += '<div class = "url">原问题网址：<a href="' + q_url + '"><h4>' + q_url + '</h4></a></div>\n'
            
            contents = ""
            answers  = self.dbHandler.getAnswersByQid(zh_qid)
            for answer in answers:
                zh_aid = answer["zh_aid"]
                author = answer["author"]
                votes  = answer["votes"]
                contents += '<div class = "content">'
                contents += '<span id = "author">%s</span>\n' % author
                contents += '<span id = "votes">赞同: %s</span>\n' % votes

                tmp_txt_dir = utils.get("tmp_answer_content_dir")
                with open(os.getcwd() + tmp_txt_dir + "%s.txt" % (zh_aid), 'r') as txt:
                    contents += str(txt.read())
                    contents += "\n"
                
                contents += '</div>'

            tmp_html_dir = utils.get("tmp_answer_content_dir") + 'html'
            print tmp_html_dir

            html         = open(os.getcwd() + tmp_html_dir + "/" + title + ".html", 'w')
            html.write(html_tpl % {'title': title, 'band': band, 'content': contents})

            # print "Start Download The image pictures ..."
            # img_urls = self.dbHandler.getImgUrls()

            # threadingSum = threading.Semaphore(20)

            # for url in img_urls:
            #     print url
            #     img_url = url["url"]
            #     t = DownloadImg(threadingSum, img_url)
            #     t.start()

            # for t in threading.enumerate(): 
            #     if t is threading.currentThread(): 
            #         continue
            #     t.join()

if __name__ == '__main__':
    toHtml = ToHtml()
    toHtml.createHtml()
