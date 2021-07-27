import timeit
from collections import deque

def print_results(count, tests):
	avg_iteration = sum(tests) / len(tests)
	print(f'Count {count:>5,} tasks {avg_iteration:.6f}s')
	return count, avg_iteration

def list_append_benchmark(count):
	def prepare():
		return deque([])

	def run(queue):
		for i in range(count):
			queue.append(i)
	
	tests = timeit.repeat(
		setup='queue = prepare()',
		stmt = 'run(queue)',
		globals=locals(),
		repeat=1000,
		number=1
	)
	return print_results(count, tests)

def list_pop_benchmark(count):
	def prepare():
		return deque(list(range(count)))

	def run(queue):
		while queue:
			queue.popleft()
	
	tests = timeit.repeat(
		setup='queue = prepare()',
		stmt='run(queue)',
		globals=locals(),
		repeat=1000,
		number=1
	)
	return print_results(count, tests)

def print_delta(before, after):
	before_count, before_time = before
	after_count, after_time = after
	growth = 1 + (after_count - before_count) / before_count
	slowdown = 1 + (after_time - before_time) / before_time
	print(f'{growth:>4.1f}x data size, {slowdown:>4.1f}x time')

print('===== append =====')
baseline = list_append_benchmark(500)
for count in (1000, 2000, 3000, 4000, 5000):
	comparison = list_append_benchmark(count)
	print_delta(baseline, comparison)

print('===== pop(0) =====')
baseline = list_pop_benchmark(500)
for count in (1000, 2000, 3000, 4000, 5000):
	comparison = list_pop_benchmark(count)
	print_delta(baseline, comparison)