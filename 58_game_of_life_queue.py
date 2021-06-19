from threading import Lock, Thread
import socket
import time
from queue import Queue


ALIVE = '*'
EMPTY = '-'

class Grid:
	def __init__(self, height, width):
		self.height = height
		self.width = width
		self.rows = []
		for _ in range(self.height):
			self.rows.append([EMPTY] * self.width)
	
	def get(self, y, x):
		return self.rows[y % self.height][x % self.width]
	
	def set(self, y, x, state):
		self.rows[y % self.height][x % self.width] = state

	def __str__(self):
		text = ''
		for row in self.rows:
			text += ''.join(row) + '\n'
		return text


class CloseableQueue(Queue):
	SENTINEL = object()

	def close(self):
		self.put(self.SENTINEL)

	def __iter__(self):
		while True:
			item = self.get()
			try:
				if item is self.SENTINEL:
					return
				yield item
			finally:
				self.task_done()


class StoppableWorker(Thread):
	def __init__(self, func, in_queue, out_queue):
		super().__init__()
		self.in_queue = in_queue
		self.out_queue = out_queue
		self.func = func

	def run(self):
		for item in self.in_queue:
			result = self.func(item)
			self.out_queue.put(result)


# if this function need threading, i need to create another queue for this
def count_neighbors(y, x, get):
	n_ = get(y - 1, x + 0)
	ne = get(y - 1, x + 1)
	e_ = get(y + 0, x + 1)
	se = get(y + 1, x + 1)
	s_ = get(y + 1, x + 0)
	sw = get(y + 1, x - 1)
	w_ = get(y + 0, x - 1)
	nw = get(y - 1, x - 1)
	neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
	count = 0
	for state in neighbor_states:
		if state == ALIVE:
			count += 1
	return count


def game_logic(state, neighbors):
	time.sleep(0.1)
	# raise OSError('Problem with I/O')
	if state == ALIVE:
		if neighbors < 2 or neighbors > 3:
			return EMPTY
	else:
		if neighbors == 3:
			return ALIVE
	return state


def game_logic_thread(item):
	y, x, state, negihbors = item
	try:
		next_state = game_logic(state, negihbors)
	except Exception as e:
		next_state = e
	return (y, x, next_state)


class SimulationError(Exception):
	pass


# difficult to read
def simulate_pipline(grid, in_queue, out_queue):
	for y in range(grid.height):
		for x in range(grid.width):
			state = grid.get(y, x)
			neighbors = count_neighbors(y, x, grid.get)
			in_queue.put((y, x, state, neighbors))
		
		in_queue.join()
		out_queue.close()

	next_grid = Grid(grid.height, grid.width)
	for item in out_queue:
		y, x, next_state = item
		if isinstance(next_state, Exception):
			raise SimulationError(y, x) from next_state
		next_grid.set(y, x, next_state)

	return next_grid	


class ColumnPrinter:
	def __init__(self):
		self.total = None
		self.head = ''
		self.count = 0

	def append(self, grid):
		grid = grid.split('\n')[:-1]
		width = len(grid[0])
		mid = width // 2
		head = ' ' * mid + str(self.count) + ' ' * (width-mid-1)
		if not self.total:
			self.total = grid
			self.head += head
		else:
			for i in range(len(self.total)):

				self.total[i] += (' | ' + grid[i])
			self.head += ' | ' + head
		self.count += 1

	def __str__(self):
		text = self.head + '\n'
		for row in self.total:
			text += ''.join(row) + '\n'
		return text


if __name__ == '__main__':
	start = time.time()

	in_queue = CloseableQueue()
	out_queue = CloseableQueue()

	threads = []
	for _ in range(5):
		thread = StoppableWorker(game_logic_thread, in_queue, out_queue)
		thread.start()
		threads.append(thread)

	grid = Grid(5, 9)
	grid.set(0, 4, ALIVE)
	grid.set(1, 5, ALIVE)
	grid.set(2, 6, ALIVE)
	grid.set(3, 7, ALIVE)
	grid.set(4, 8, ALIVE)
	grid.set(1, 6, ALIVE)
	grid.set(2, 8, ALIVE)
	grid.set(1, 3, ALIVE)
	grid.set(2, 1, ALIVE)
	grid.set(2, 2, ALIVE)
	grid.set(3, 5, ALIVE)
	grid.set(3, 4, ALIVE)

	columns = ColumnPrinter()
	for i in range(5):
		columns.append(str(grid))
		grid = simulate_pipline(grid, in_queue, out_queue)

	print(columns)

	for thread in threads:
		in_queue.close()
	for thread in threads:
		thread.join()

	end = time.time()
	print(f'runtime {end-start:.3f} s')