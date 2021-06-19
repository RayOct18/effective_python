from queue import Queue
from threading import Thread
import time

def download(x):
	time.sleep(0.01)
	return x

def resize(x):
	time.sleep(0.01)
	return x

def upload(x):
	time.sleep(0.01)
	return x


class CloseableQueue(Queue):
	SENTINEL = object()

	def close(self):
		self.put(self.SENTINEL)

	def __iter__(self):
		while True:
			item = self.get()
			try:
				if item is self.SENTINEL:
					return  # exit
				yield item
			finally:
				self.task_done()


class StoppableWorker(Thread):
	def __init__(self, func, in_queue, out_queue):
		super().__init__()
		self.func = func
		self.in_queue = in_queue
		self.out_queue = out_queue
	
	def run(self):
		for item in self.in_queue:
			result = self.func(item)
			self.out_queue.put(result)


def start_threads(count, *args):
	threads = [StoppableWorker(*args) for _ in range(count)]
	for thread in threads:
		thread.start()
	return threads


def stop_threads(closable_queue, threads):
	for _ in threads:
		closable_queue.close()

	closable_queue.join()

	for thread in threads:
		thread.join()

start = time.time()

download_queue = CloseableQueue()
resize_queue = CloseableQueue()
upload_queue = CloseableQueue()
done_queue = CloseableQueue()

download_threads = start_threads(1, download, download_queue, resize_queue)
resize_threads = start_threads(1, resize, resize_queue, upload_queue)
upload_threads = start_threads(1, upload, upload_queue, done_queue)


for _ in range(1000):
	download_queue.put(object())

stop_threads(download_queue, download_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

end = time.time()
print(done_queue.qsize(), f'items finished in {end-start:.3f} sec')


start = time.time()

download_queue = CloseableQueue()
resize_queue = CloseableQueue()
upload_queue = CloseableQueue()
done_queue = CloseableQueue()

download_threads = start_threads(3, download, download_queue, resize_queue)
resize_threads = start_threads(4, resize, resize_queue, upload_queue)
upload_threads = start_threads(5, upload, upload_queue, done_queue)


for _ in range(1000):
	download_queue.put(object())

stop_threads(download_queue, download_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

end = time.time()
print(done_queue.qsize(), f'items finished in {end-start:.3f} sec')