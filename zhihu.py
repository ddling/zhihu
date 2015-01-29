from question import Question
from downloadPage import DownloadThread
import threading

class Zhihu:

    def __init__(self):

        questionTxt = open("readlist.txt")

        threadingSum = threading.Semaphore(20)

        for url in questionTxt:
            t = DownloadThread(threadingSum, url.replace("\n", ""))
            t.start()

        for t in threading.enumerate():
            if t is threading.currentThread():
                continue
            t.join()

if __name__ == "__main__":
    zhihu = Zhihu()
