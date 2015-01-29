from question import Question
from toHtml import ToHtml

question = Question("http://www.zhihu.com/question/27848661")
title = question.get_title()
print title
detail = question.get_detail()
print detail
answer_num = question.get_answer_num()
print answer_num
tags = question.get_tags()
for tag in tags:
    print tag
# authors = question.get_all_authors()
# for author in authors:
#     print author
# votes = question.get_all_votes()
# for vote in votes:
#     print vote
# answers = question.get_all_answers()
# for answer in answers:
#     print answer
# toHtml = ToHtml("http://www.zhihu.com/question/27848661")
# toHtml.answerToHtml()

# question = Question("http://www.zhihu.com/question/25029518")
# urls = question.get_all_pics()
# question.download_all_pics(urls)
