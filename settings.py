import shutil
from os.path import exists

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from yaml import load, dump

try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

gauth = drive = config = None


def init():
	global gauth, drive, config
	
	# gauth = GoogleAuth()
	# gauth.LocalWebserverAuth()
	# drive = GoogleDrive(gauth)
	
	if not exists("config.yaml"):
		shutil.copyfile("default_config.yaml", "config.yaml")
		
	load_config(open("config.yaml"))


def add_directory(path):
	global config
	
	# Do not include a new path if it is already included within a currently listed directory
	# Otherwise, remove any directories contained by the new path
	for entry in config.directories:
		# A directory can only possibly be contained by an entry if the entry contains less subdirectories
		if entry.count('/') < path.count('/'):
			if path.contains(entry):
				return
		else:
			# If an entry is already listed, and is contained within the new path, no higher directory can be listed already
			# Because of this logic, we can use the same loop to remove lower directories contained by the new directory
			if entry.contains(path):
				config.directories.remove(entry)
				
	config.directories.append(path)
	
	save_config()
	

def load_config(config_file):
	global config
	
	config = load(config_file, Loader=Loader)


def save_config():
	with open("config.yaml", 'w') as file:
		dump(config, file)
