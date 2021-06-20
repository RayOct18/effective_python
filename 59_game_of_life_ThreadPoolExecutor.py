import time
from threading import Lock
from concurrent.futures import ThreadPoolExecutor


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


class LockingGrid(Grid):
	def __init__(self, height, width):
		super().__init__(height, width)
		self.lock = Lock()

	def get(self, y, x):
		with self.lock:
			return super().get(y, x)

	def set(self, y, x, state):
		with self.lock:
			return super().set(y, x, state)

	def __str__(self):
		return super().__str__()


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
	if state == ALIVE:
		if neighbors < 2 or neighbors > 3:
			return EMPTY
	else:
		if neighbors == 3:
			return ALIVE
	return state


def step_call(y, x, get, set):
	state = get(y, x)
	neighbors = count_neighbors(y, x, get)
	next_state = game_logic(state, neighbors)
	set(y, x, next_state)


def simulate_pool(pool, grid):
	next_grid = Grid(grid.height, grid.width)

	futures = []
	for y in range(grid.height):
		for x in range(grid.width):
			args = (y, x, grid.get, next_grid.set)
			future = pool.submit(step_call, *args)
			futures.append(future)

	for future in futures:
		future.result()

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
	with ThreadPoolExecutor(max_workers=10) as pool:
		for i in range(4):
			columns.append(str(grid))
			grid = simulate_pool(pool, grid)

	print(columns)

	end = time.time()
	print(f'runtime {end-start:.3f} s')