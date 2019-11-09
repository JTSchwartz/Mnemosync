import shutil
from os.path import exists

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from yaml import load, dump

try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

# output = dump(data, Dumper=Dumper)

gauth = drive = config = None


def init():
	global gauth, drive, config
	
	gauth = GoogleAuth()
	gauth.LocalWebserverAuth()
	drive = GoogleDrive(gauth)
	
	if not exists("config.yaml"):
		shutil.copyfile("default_config.yaml", "config.yaml")
		
	load_config(open("config.yaml"))


def load_config(config_file):
	global config
	
	config = load(config_file, Loader=Loader)
