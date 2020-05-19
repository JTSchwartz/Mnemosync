import re

import settings


def test_excluded_files(path):
	for exclude in settings.config["fileTypeExclusions"]:
		if path.endswith(exclude):
			return True
	
	for exclude in settings.config["fileNameExclusions"]:
		if re.search(exclude, path):
			return True
	
	return False


def test_excluded_paths(path):
	for exclude in settings.config["directoryExclusions"]:
		if re.search(exclude, path):
			return True
	
	return False
