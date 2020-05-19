from os import walk as traverse
from threader import DirectoryManager, SyncManager
from file_management import *
from utils import *


def main():
	settings.init()
	
	# Needed for GDrive implementation
	# if settings.drive is None:
	# 	print("Err")
	
	directories = set()
	
	for directory in settings.config["directories"]:
		for dir_name, _, _ in traverse(directory):
			if test_excluded_paths(dir_name):
				continue
			
			directories.add(dir_name)
			
	sync_manager = SyncManager(directories)
	directory_manager = DirectoryManager(sync_manager, directories)
	
	managers = [directory_manager, sync_manager]
	
	map(lambda thread: thread.start(), managers)
	map(lambda thread: thread.join(), managers)


if __name__ == '__main__':
	main()
