import datetime
import time

from concurrency.ThreadPool import ThreadPool
from concurrency.workers.WorkerCollections import WorkerCollections
from tools.Logger import init_success


class Pipeline:

    def __init__(self, spider, n_git_threads, n_file_threads, worker_save=None):
        self.n_git_threads = n_git_threads
        self.n_file_threads = n_file_threads
        self.worker_menu = WorkerCollections(spider)
        self.pool = ThreadPool(spider, n_git_threads, n_file_threads, worker_save)
        self.logger = init_success()

    def search_collections(self, collections):
        self.logger.info('Start collection search,  %s wrk threads' % self.n_git_threads)
        start = time.time()
        repositories = self.worker_menu.crawl_collections(collections)
        self.logger.info('Repositories found: %s' % len(repositories))
        end = time.time()
        duration = str(datetime.timedelta(seconds=end - start))
        self.logger.info('Finished collection search  in %s' % duration)
        return repositories

    def clone_repositories(self, repo_urls, file_ending_whitelist):
        self.logger.info(
            'Start repository cloning, %s git threads, %s file threads' % (self.n_git_threads, self.n_file_threads))
        start = time.time()
        repositories = self.pool.start_workers_git(repo_urls, file_ending_whitelist)
        end = time.time()
        duration = str(datetime.timedelta(seconds=end - start))
        self.logger.info('Finished repository cloning in %s' % duration)
        return repositories
