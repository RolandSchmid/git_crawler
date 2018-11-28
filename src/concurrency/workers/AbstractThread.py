from threading import Thread


class AbstractThread(Thread):

    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True

    def stop(self):
        self.running = False
