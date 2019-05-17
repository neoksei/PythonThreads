import threading
import json
import lockfile
import os


class WritingThread(threading.Thread):

    def __init__(self, fname, new_items, thread_mutex):
        threading.Thread.__init__(self)
        self.fname = fname
        self.new_items = new_items
        self.thread_mutex = thread_mutex

    def run(self):
        ipc_lock = lockfile.FileLock(self.fname)

        ipc_lock.acquire()
        self.thread_mutex.acquire()

        if not os.path.exists(self.fname):
            with open(self.fname, 'w') as f:
                f.write('[]')

        with open(self.fname, 'r') as f:
            old_items = json.load(f)
        self.thread_mutex.release()
        ipc_lock.release()

        final_items = [item for item in self.new_items if item not in old_items] + old_items

        ipc_lock.acquire()
        self.thread_mutex.acquire()
        with open(self.fname, 'w') as f:
            json.dump(final_items, f, indent=4)
        self.thread_mutex.release()
        ipc_lock.release()
