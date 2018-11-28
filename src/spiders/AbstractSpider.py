from abc import abstractmethod, ABC
from time import sleep

import requests
from fake_useragent import UserAgent

from tools.Logger import init_main

logger = init_main()


# WebReader
class WebReader(requests.Session):
    ua = UserAgent()

    def __init__(self, home_url):
        super().__init__()
        self.headers['User-Agent'] = self.ua.random
        self.headers['Accept'] = '*/*'
        self.headers['Origin'] = home_url
        self.headers['Referer'] = home_url

    def get_html(self, url, retry=False):
        data = None
        resp = None

        while not data:
            try:
                resp = self.get(url)

                eresult = resp.headers.get('X-eresult', -1)
                if resp.status_code != 200:
                    raise Exception("HTTP %s EResult %s\n%s" % (resp.status_code, eresult, resp.text))

            except Exception as e:
                if resp is None or resp.status_code >= 500:
                    sleep(2)
                    continue
            else:
                data = resp.text

            if not retry:
                break

            if not data:
                sleep(1)

        return data


class AbstractSpider(ABC):

    def __init__(self, main_url):
        self.main_url = main_url
        self.reader = WebReader(main_url)

    @abstractmethod
    def process_collection(self, url):
        pass

    @abstractmethod
    def process_repository(self, suffix):
        pass
