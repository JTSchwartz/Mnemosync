import threading


class Threader(threading.Thread):
	
	def run(self):
		print("Thread Started")