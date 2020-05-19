import os
import time
from math import floor
from queue import Queue
from threading import Thread, Event

from utils import *

SYNC_DISABLED = Event()
SYNC_INTERVAL = 3
SYNC_THREAD_LIMIT = 1

directory_queue = Queue()
completed_queue = Queue()


class SyncManager(Thread):
	
	def __init__(self, directories):
		global directory_queue
		
		q = Queue()
		[q.put(i) for i in directories]
		directory_queue = q
		super().__init__()
	
	def run(self):
		threads = []
		
		for count in range(floor(directory_queue.qsize() / 15)):
			t = SyncThread()
			t.start()
			threads.append(t)
		
		while not SYNC_DISABLED.wait(SYNC_INTERVAL):
			while not completed_queue.empty():
				directory_queue.put(completed_queue.get())
		
		map(lambda thread: thread.join(), threads)
	
	@staticmethod
	def add_directory(path):
		directory_queue.put(path)


class SyncThread(Thread):
	
	def run(self):
		while not SYNC_DISABLED.wait(SYNC_INTERVAL):
			self.job(time.time() - (SYNC_INTERVAL * 1000))
	
	@staticmethod
	def job(sync_time):
		while not directory_queue.empty():
			base_path = directory_queue.get()
			
			for entry in os.listdir(base_path):
				path = base_path + "\\" + entry
				if not test_excluded_files(path) and sync_time <= os.path.getmtime(path):
					print("Passed: ", entry)
			
			completed_queue.put(base_path)


class DirectoryManager(Thread):
	all_directories: set
	sync_manager: SyncManager
	
	def __init__(self, sync_manager, dir_set):
		self.sync_manager = sync_manager
		self.all_directories = dir_set
		super().__init__()
	
	def run(self):
		while not SYNC_DISABLED.wait(SYNC_INTERVAL):
			for directory in self.all_directories:
				for dir_name, _, _ in os.walk(directory):
					if test_excluded_paths(dir_name) or dir_name in self.all_directories:
						continue
					
					self.all_directories.add(dir_name)
					self.sync_manager.add_directory(dir_name)


if __name__ == '__main__':
	assert False
