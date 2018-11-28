import contextlib
import sys
from threading import Lock

from tqdm import tqdm


class DummyTqdmFile(object):
    """Dummy file-like that will write to tqdm"""
    file = None

    def __init__(self, file):
        self.file = file

    def write(self, x):
        # Avoid print() second call (useless \n)
        if len(x.rstrip()) > 0:
            tqdm.write(x, file=self.file)

    def flush(self):
        return getattr(self.file, "flush", lambda: None)()


@contextlib.contextmanager
def std_out_tqdm():
    orig_out_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = map(DummyTqdmFile, orig_out_err)
        yield orig_out_err[0]
    # Relay exceptions
    except Exception as exc:
        raise exc
    # Always restore sys.stdout/err if necessary
    finally:
        sys.stdout, sys.stderr = orig_out_err


class ProgressBar:
    lock = Lock()

    def __init__(self, desc, total, file=None, complete=0):
        self.file = file
        self.init(desc, total, complete)
        self.frm = '{desc:<20} {percentage:3.0f}% |{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]'

    def __start(self):
        # leave=True for progressbar to vanish immediately after completion
        self.pbar = tqdm(file=self.file, ascii=True, leave=False, dynamic_ncols=True,
                         desc=self.desc, initial=0, total=1, bar_format=self.frm)

    def init(self, desc, total, complete=0):
        self.desc = desc
        self.total = total
        self.complete = complete
        self.pbar = None

    def add(self, n):
        if self.lock.acquire():
            self.total += n
            self.lock.release()

    def set_file(self, file):
        self.file = file

    def finishOne(self):
        if self.lock.acquire():
            if (not self.pbar): self.__start()
            self.complete += 1
            cur_perc = self.complete / self.total
            self.pbar.n = cur_perc
            self.pbar.refresh()
            self.lock.release()

    def close(self):
        try:
            if (self.pbar): self.pbar.close()
        except Exception:
            pass

# Redirect stdout to tqdm.write() (don't forget the 'as orig_stdout')
# with std_out_err_redirect_tqdm() as orig_stdout:
#     asd = ProgressBar('desc', 200, file=orig_stdout)
#     for i in range(200):
#         asd.finishOne()
#         time.sleep(0.2)
