from concurrency.workers.AbstractThread import AbstractThread
from tools.Logger import init_main


class WorkerCollections(AbstractThread):

    def __init__(self, spider):
        super().__init__()
        self.stop()
        self.spider = spider()
        self.name = 'Worker Collections'
        self.logger = init_main()

    def crawl_collections(self, collections):
        self.logger.info('Scanning for repositories: %s' % self.spider.main_url)
        result = []
        for url in collections:
            result += self.spider.process_collection(url)
        return result
