

class Counter:
	def __init__(self):
		self.count = 0 
	
	def increment(self, offset):
		self.count += offset

def worker(sensor_index, how_many, counter):
	for _ in range(how_many):
		counter.increment(1)
		"""
		# Data races

		value_a = getter(counter, 'count')
		value_b = getter(counter, 'count')
		result_a = value_a + 1
		setter(counter, 'count', result_a)
		result_b = value_b + 1
		setter(counter, 'count', result_b) # override the value
		"""


from threading import Thread

how_many = 10 ** 5
counter = Counter()

threads = []
for i in range(5):
	thread = Thread(target=worker,
					args=(i, how_many, counter))
	thread.start()
	threads.append(thread)

for thread in threads:
	thread.join()

expected = how_many * 5
found = counter.count
print(f'Counter should be {expected}, got {found}')



from threading import Lock

class LockingCounter:
	def __init__(self):
		self.lock = Lock()
		self.count = 0
	def increment(self, offset):
		with self.lock:
			self.count += offset

how_many = 10 ** 5
counter = LockingCounter()

threads = []
for i in range(5):
	thread = Thread(target=worker,
					args=(i, how_many, counter))
	thread.start()
	threads.append(thread)

for thread in threads:
	thread.join()

expected = how_many * 5
found = counter.count
print(f'Counter should be {expected}, got {found}')