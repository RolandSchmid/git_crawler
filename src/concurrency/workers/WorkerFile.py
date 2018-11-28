import os
from queue import Empty
from time import sleep

from Config import Config
from concurrency.workers.AbstractThread import AbstractThread
from tools.JsonTools import JsonTools
from tools.Logger import init_main

logger = init_main()


class WorkerFile(AbstractThread):

    def __init__(self, queue_repositories):
        super().__init__()
        self.name = 'Worker File'
        self.queue_repositories = queue_repositories

    def run(self):
        while self.running:
            try:
                repository = self.queue_repositories.get(False)
                self.__save_repository(repository)
                self.queue_repositories.task_done()
            except Empty:
                sleep(1)
                continue

    def __save_repository(self, repository):
        filename = os.path.join(Config.get_dir_repos(), repository.encode_url() + '.json')
        data = JsonTools.save_repository(repository)
        with open(filename, 'w', encoding='utf-8') as outfile:
            outfile.write(data)
        logger.debug('Saved repository: %s' % repository.url)

    def stop(self):
        super().stop()
