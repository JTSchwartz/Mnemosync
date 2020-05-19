import re
from os import walk as traverse
from queue import Queue
from threader import SyncManager
from file_management import *


def main():
	settings.init()
	
	# Needed for GDrive implementation
	# if settings.drive is None:
	# 	print("Err")
	
	queue = Queue()
	# print(all_files())
	for directory in settings.config["directories"]:
		for dirName, subdirList, fileList in traverse(directory):
			if test_excluded_paths(dirName):
				continue
			
			queue.put(dirName)
			
	manager = SyncManager(queue)
	manager.start()
	manager.join()


def test_excluded_paths(path):
	for exclude in settings.config["directoryExclusions"]:
		if re.search(exclude, path):
			return True
	
	return False


if __name__ == '__main__':
	main()
