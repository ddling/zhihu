import ConfigParser
import requests

class Session:

    def get_session(self):

        config = ConfigParser.ConfigParser()
        config.read("config.ini")
        email = config.get("zhihu", "email")
        password = config.get("zhihu", "password")
        session = requests.session()
        login_data = {"email": email, "password": password}
        header = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
        'Host': "www.zhihu.com",
        'Referer': "http://www.zhihu.com/",
        'X-Requested-With': "XMLHttpRequest"
    }
        request = session.post('http://www.zhihu.com/login', data = login_data, headers = header)
        if request.json()["r"] == 1:
            raise Exception("login failed.")
        return session

