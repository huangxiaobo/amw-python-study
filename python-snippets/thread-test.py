# /usr/bin/env python
# -*- encoding=utf-8 -*-

import subprocess
import time
import logging
import threading
import signal
import sys

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

g_threads = []


def handler(signal, frame):
    global g_threads
    for t in g_threads:
        t.kill_received = True
    sys.exit(0)


class MyJob(threading.Thread):
    def __init__(self, cmd):
        super(MyJob, self).__init__()
        self.cmd = cmd
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            process = subprocess.Popen(self.cmd.split(), close_fds=True,
                                       shell=False)
            process.wait()
            logger.info("Execute \"%s\" sucessful, returncode: %s" % (
                self.cmd, process.returncode))
            time.sleep(1)


class MyJob2(threading.Thread):
    pass


def main():
    global g_threads

    cmds = [
        'echo 1',
    ]

    for cmd in cmds:
        t = MyJob(cmd)
        g_threads.append(t)
        t.setDaemon(True)
        t.start()

    while True:
        alive = False
        for t in g_threads:
            alive = alive or t.isAlive()
        if not alive:
            break


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    main()
