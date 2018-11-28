from queue import Queue

from concurrency.workers.WorkerGit import WorkerGit
from tools.Logger import init_main
from tools.Progressbar import std_out_tqdm, ProgressBar


class ThreadPool:

    def __init__(self, spider, n_git_threads, n_file_threads, worker_file=None):
        self.spider = spider
        self.n_git_threads = n_git_threads
        self.n_file_threads = n_file_threads
        self.queue_repositories = Queue()
        self.queue_out = Queue()
        self.workers_git = list()
        self.worker_file = worker_file(self.queue_out)
        self.repositories = []
        self.logger = init_main()

    def start_workers_git(self, repo_urls=None, file_ending_whitelist=None):
        self.__init_wrk_repository(repo_urls, file_ending_whitelist)
        self.logger.info('Starting WorkerGit')

        with std_out_tqdm() as orig_stdout:
            self.progress_bar.set_file(orig_stdout)
            for w in self.workers_git:
                w.start()
            self.worker_file.start()
            self.queue_repositories.join()
            self.progress_bar.close()
        for w in self.workers_git:
            w.stop()

        self.progress_bar.close()
        self.logger.info('Finished reading repositories')

        self.queue_out.join()
        self.worker_file.stop()
        self.logger.info('Finished saving repositories')
        return self.repositories

    def __init_wrk_repository(self, repo_urls, file_ending_whitelist):
        if repo_urls:
            for url in set(repo_urls):
                self.queue_repositories.put(url)
        self.progress_bar = ProgressBar('Processing repositories', len(repo_urls))
        for i in range(self.n_git_threads):
            # self.logger.debug('New WorkerRepository: ID=%s' % i)
            w = WorkerGit(self.spider, self.progress_bar, i, self.queue_repositories, self.queue_out,
                          self.repositories, file_ending_whitelist)
            self.workers_git.append(w)
