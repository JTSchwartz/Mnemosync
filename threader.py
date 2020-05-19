import os
import time
import re
import settings
from math import floor
from queue import Queue
from threading import Thread, Event

SYNC_DISABLED = Event()
SYNC_INTERVAL = 3
SYNC_THREAD_LIMIT = 1

directory_queue = Queue()
completed_queue = Queue()


class SyncThread(Thread):
	
	def __init__(self):
		super().__init__()
	
	def run(self):
		while not SYNC_DISABLED.wait(SYNC_INTERVAL):
			self.job(time.time() - (300 * 1000))
	
	def job(self, sync_time):
		while not directory_queue.empty():
			base_path = directory_queue.get()
			
			for entry in os.listdir(base_path):
				path = base_path + "\\" + entry
				if not self.test_excluded_files(path) and sync_time <= os.path.getmtime(path):
						
					print("Passed: ", entry)
					
			completed_queue.put(base_path)
						
	@staticmethod
	def test_excluded_files(path):
		for exclude in settings.config["fileTypeExclusions"]:
			if path.endswith(exclude):
				return True
		
		for exclude in settings.config["fileNameExclusions"]:
			if re.search(exclude, path):
				return True
		
		return False


class SyncManager(Thread):
	
	def __init__(self, directories):
		global directory_queue
		
		directory_queue = directories
		super().__init__()
	
	def run(self):
		threads = []
		
		for count in range(floor(directory_queue.qsize() / 15)):
			t = SyncThread()
			t.start()
			threads.append(t)
		
		while not SYNC_DISABLED.wait(SYNC_INTERVAL):
			# print("Q")
			while not completed_queue.empty():
				directory_queue.put(completed_queue.get())
		
		map(lambda thread: thread.join(), threads)
	
	@staticmethod
	def add_directory(path):
		directory_queue.put(path)


if __name__ == '__main__':
	assert False
