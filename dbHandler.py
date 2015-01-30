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

        cur = self.conn.cursor()
        sql = "INSERT INTO zh_answer VALUES (NULL, %d, '%s', '%s', '%s')" % (zh_qid, url, author, votes)
        print sql
        cur.execute(sql)
        self.conn.commit()
        cur.close()

    def insertNewImgUrl(self, zh_aid, url):
        
        cur = self.conn.cursor()
        sql = "INSERT INTO zh_img_url VALUES (NULL, %d, '%s')" % (zh_aid, url)

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

    def getQueIdByUrl(self, url):

        cur = self.conn.cursor()
        sql = "SELECT zh_qid FROM zh_question WHERE url = '%s'" % url
        cur.execute(sql)
        resultSet = cur.fetchone()
        for result in resultSet:
            return result

    def getAnsIdByUrl(self, url):

        cur = self.conn.cursor()
        sql = "SELECT zh_aid FROM zh_answer WHERE url = '%s'" % url
        cur.execute(sql)
        resultSet = cur.fetchone()
        for result in resultSet:
            return result

    def getQuestions(self):

        cur = self.conn.cursor()
        sql = "SELECT * FROM zh_question"
        cur.execute(sql)
        resultSet = cur.fetchall()
        for row in resultSet:
            question = {}
            question["zh_qid"] = row[0]
            question["url"] = row[1]
            question["title"] = row[2]
            question["detail"] = row[3]
            question["tags"] = row[4]
            question["followers"] = row[5]
            question["answerNum"] = row[6]
            yield question

    def getAnswersByQid(self, zh_qid):

        cur = self.conn.cursor()
        sql = "SELECT * FROM zh_answer WHERE zh_qid = %d" % (zh_qid)
        cur.execute(sql)
        resultSet = cur.fetchall()
        for row in resultSet:
            answer = {}
            answer["zh_aid"] = row[0]
            answer["zh_qid"] = row[1]
            answer["url"] = row[2]
            answer["author"] = row[3]
            answer["votes"] = row[4]
            yield answer

    def getImgUrls(self):

        cur = self.conn.cursor()
        sql = "SELECT * FROM zh_img_url"
        cur.execute(sql)
        resultSet = cur.fetchall()
        for row in resultSet:
            img = {}
            img["zh_iid"] = row[0]
            img["zh_aid"] = row[1]
            img["url"] = row[2]
            yield img
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    dbHandler = DbHandler()
    for question in dbHandler.getQuestions():
        print question
        zh_qid = question["zh_qid"]
        for answer in dbHandler.getAnswersByQid(zh_qid):
            print answer
