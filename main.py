from file_management import *
from os import walk as traverse
import re
from settings import *
from threader import Threader


def run_threads():
	directories = config["directories"]
	
	threads = []
	
	for loop in range(len(directories)):
		t = Threader()
		threads.append(t)
	
	map(lambda thread: thread.join(), threads)


def main():
	settings.init()
	
	# Needed for GDrive implementation
	# if settings.drive is None:
	# 	print("Err")

	# print(all_files())
	directory = "C:\\Users\\jtsch\\Workspace"
	for dirName, subdirList, fileList in traverse(directory):
		if test_excluded_paths(dirName):
			continue
		
		print('Found directory: %s' % dirName)
		for file in fileList:
			if test_excluded_files(file):
				continue
				
			print('\t%s' % file)


def test_excluded_paths(path):
	for exclude in settings.config["directoryExclusions"]:
		if re.search(exclude, path):
			return True
	
	return False


def test_excluded_files(path):
	for exclude in settings.config["fileTypeExclusions"]:
		if path.endswith(exclude):
			return True
	
	for exclude in settings.config["fileNameExclusions"]:
		if re.search(exclude, path):
			return True
	
	return False


if __name__ == '__main__':
	main()
