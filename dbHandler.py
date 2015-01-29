import sqlite3

class DbHandler:

    def __init__(self):
        self.conn                 = sqlite3.connect("sql.db")
        self.conn.isolation_level = None

    def insertNewQuestion(self, question = {}):
        url       = question["url"]
        title     = question["title"]
        detail    = question["detail"]
        followers = question["followers"]
        tags      = question["tags"]
        answerNum = question["answerNum"]

        cur = self.conn.cursor()
        sql = "INSERT INTO zh_question VALUES (NULL, '%s', '%s', '%s', '%s', %d, %d)" % (url, title, detail, tags, followers, answerNum)
        print sql
        cur.execute(sql)
        self.conn.commit()
        cur.close()

    def insertNewAnswer(self, answer = {}):
        zh_qid   = answer["zh_qid"]
        url      = answer["url"]
        author   = answer["author"]
        votes    = answer["votes"]
        contents = answer["contents"]

        cur = self.conn.cursor()
        sql = "INSERT INTO zh_answer VALUES (NULL, %d, '%s', '%s', %d, '%s')" % (zh_qid, url, author, votes, contents)
        cur.execute(sql)
        self.conn.commit()
        cur.close()

    def hasQuestion(self, url):
        
        cur = self.conn.cursor()
        sql = "SELECT * FROM zh_question WHERE url = '%s'" % url
        cur.execute(sql)
        resultSet = cur.fetchall()
        if len(resultSet) > 0:
            return True

        return False

    def getAnsIdByUrl(self, url):

        cur = self.conn.cursor()
        sql = "SELECT zh_qid FROM zh_question WHERE url = '%s'" % url
        cur.execute(sql)
        resultSet = cur.fetchone()
        for result in resultSet:
            return result
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    dbHandler = DbHandler()
    question = {"url": "www.baidu.com", "title": "title", "detail": "detail", "followers": 12, "answerNum": 100}
    dbHandler.insertNewQuestion(question)
