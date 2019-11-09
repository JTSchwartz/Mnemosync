from settings import *
from file_management import *
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
	
	if settings.drive is None:
		print("Err")


# print(all_files())


if __name__ == '__main__':
	main()
