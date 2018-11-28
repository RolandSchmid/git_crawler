from collections import defaultdict


class Repository:

    def __init__(self, url, latest_commit, topics, endings=None, code=None):
        self.url = url
        self.latest_commit = latest_commit
        self.topics = topics
        self.endings = endings if endings is not None else defaultdict(int)
        self.code = code if code is not None else []

    def encode_url(self):
        return self.url.replace('/', '_')
