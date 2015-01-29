from question import Question

class ToHtml:

    html_file = None
    question = None

    def __init__(self, url):

        self.question = Question(url)
        title = self.question.get_title()

        flag = False
        self.html_file = open(store_dir + "/" + title + ".html", 'w')

    def answerToHtml(self):

        title = self.question.get_title()
        detail = self.question.get_detail()
        tags = self.question.get_tags()
        answers = self.question.get_all_answers()
        votes = self.question.get_all_votes
        authors = self.question.get_all_authors()
        self.html_file.write(u'''<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>test</title></head><body>
''')
        self.html_file.write("<h3>" + title + "</h3>")
        self.html_file.write("<h5>" + detail + "</h5>")
        self.html_file.write('<div class="zm-tag">')
        for tag in tags:
            self.html_file.write("<span>" + tag + "</span>")
        self.html_file.write("</div>")
        self.html_file.write('<div class="answers">')
        for j in range(min(self.question.get_answer_num(), 50)):
            self.html_file.write('<div class="answer">')
            self.html_file.write('<div class="author">' + authors[j] + '</div>')
            self.html_file.write(u'''<div class="ans"> + answers[j] + </div>''')
            self.html_file.write("</div>")
        self.html_file.write('</div></body>')
        self.close()
        
    def close(self):

        self.html_file.close()
