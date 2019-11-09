import settings


def all_files(subdirectory="root"):
	
	return settings.drive.ListFile({'q': f"'root/{settings.config['gDrive']}{subdirectory}' in parents and trashed=false"}).GetList()

# def check_for_directory():

# def create_directory():

# def update_directory():

# def delete_directory():

# def rename_directory():

# def check_for_file():

# def create_file():

# def update_file():

# def delete_file():

# def rename_file():
