import codecs
import os
import re
from queue import Empty, Queue
from time import sleep

import git
from git import GitCommandError

from Config import Config
from concurrency.workers.AbstractThread import AbstractThread
from tools.Logger import init_main

logger = init_main()


class WorkerGit(AbstractThread):

    def __init__(self, spider, progress_bar, index, queue_repositories, queue_out, repositories, file_ending_whitelist):
        super().__init__()
        self.spider = spider()
        self.progress_bar = progress_bar
        self.name = 'Worker Git #' + str(index)
        self.queue_repositories = queue_repositories
        self.queue_out = queue_out
        self.file_ending_whitelist = file_ending_whitelist
        self.repositories = repositories

    def run(self):
        while self.running:
            try:
                url = self.queue_repositories.get(False)
            except Empty:
                sleep(1)
                continue
            self.__run_repository(url)

    def stop(self):
        super().stop()

    def __run_repository(self, suffix):
        repository = self.spider.process_repository(suffix)
        if repository:
            logger.debug('Pull repository: %s' % suffix)
            while not self.__git_pull(repository):
                sleep(1)
            self.queue_out.put(repository)
            self.repositories.append(repository)
        else:
            logger.error('Could not parse repository: %s' % suffix)

        self.progress_bar.finishOne()
        self.queue_repositories.task_done()

    def __git_pull(self, repository):
        path = os.path.join(Config.get_dir_repos(), Config.get_timestamp(), repository.encode_url())
        os.makedirs(path)
        try:
            # Clone repository
            git.Git(path).clone(self.spider.main_url + repository.url + '.git')
            self.__parse_repo(repository, path)
            return True
        except GitCommandError as e:
            logger.error('Error: ' + str(e))
            return False

    def __parse_repo(self, repository, path):
        queue_directories = Queue()
        queue_directories.put(path)
        while not queue_directories.empty():
            folder = queue_directories.get()
            for file in os.listdir(folder):
                filename = os.path.join(folder, file)
                if os.path.isdir(filename):
                    if not filename.endswith('.git'):
                        queue_directories.put(filename)
                else:
                    ending = ''
                    if '.' in file:
                        ending = file.split('.')[-1].lower()
                        repository.endings[ending] += 1
                    if ending in self.file_ending_whitelist:
                        repository.code += self.__parse_file(filename)

    @staticmethod
    def __parse_file(file):
        words = []
        try:
            with codecs.open(file, "r", encoding='utf-8', errors='ignore') as infile:
                lines = infile.readlines()
            for line in lines:
                # Remove special characters
                words += re.findall(r"[\w']+", line)
        except UnicodeDecodeError as e:
            logger.error("UnicodeDecodeError: " + str(e) + " " + file)
        return words
