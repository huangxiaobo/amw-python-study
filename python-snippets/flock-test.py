import time
import fcntl

def do_something():
	time.sleep(10)

class Lock(object):
	LOCK_FILE = '/tmp/test.lock'

	def __init__(self):
		self.lock_fp = None

	def __enter__(self):
		self.lock_fp = open(self.LOCK_FILE, "a+")
		fcntl.flock(self.lock_fp, fcntl.LOCK_EX)


	def __exit__(self, *args):
		if self.lock_fp is not None:
			fcntl.flock(self.lock_fp, fcntl.LOCK_UN)
			self.lock_fp.close()
			self.lock_fp = None


def main():
	with Lock():
		do_something()

if __name__ == "__main__":
	main()
