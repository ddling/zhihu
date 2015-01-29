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
        answerNum = question["answerNum"]

        cur = self.conn.cursor()
        sql = "INSERT INTO zh_question VALUES (NULL, '%s', '%s', '%s', %d, %d)" % (url, title, detail, followers, answerNum)
        print sql
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
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    dbHandler = DbHandler()
    question = {"url": "www.baidu.com", "title": "title", "detail": "detail", "followers": 12, "answerNum": 100}
    dbHandler.insertNewQuestion(question)
