import logging

from tqdm import tqdm

from Config import Config

formatter = logging.Formatter('%(asctime)s [%(threadName)s] %(levelname)s - %(message)s')


class TqdmLoggingHandler(logging.Handler):

    def __init__(self, level=logging.NOTSET):
        super(self.__class__, self).__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            # TODO Check if debug, then stack logs and release at once
            tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def _init_logger(log_file, name, file_level=logging.WARN, console=False, cons_level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file, encoding="UTF8")
    fh.setLevel(file_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if console:
        ch = TqdmLoggingHandler()
        ch.setLevel(cons_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger


c = Config()

log_file_main = c.get_dir_out() + 'git_crawl_error.log'
instance_main = None


def init_main():
    global instance_main
    if instance_main:
        return instance_main
    instance_main = _init_logger(log_file_main, 'git_crawl_main', file_level=logging.WARN, console=True,
                                 cons_level=logging.DEBUG)
    return instance_main


log__file_success = c.get_dir_out() + 'git_crawl_success.log'
instance_success = None


def init_success():
    global instance_success
    if instance_success:
        return instance_success
    instance_success = _init_logger(log__file_success, 'git_crawl_success', file_level=logging.INFO, console=True)
    return instance_success
