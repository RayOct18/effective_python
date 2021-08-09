import random
import timeit
from bisect import bisect_left

size = 10 ** 5
iterations = 1000

data = list(range(size))
to_lookup = [random.randint(0, size)
			 for _ in range(iterations)]

def run_linear(data, to_lookup):
	for index in to_lookup:
		data.index(index)

def run_bisect(data, to_lookup):
	for index in to_lookup:
		bisect_left(data, index)

baseline = timeit.timeit(
	stmt='run_linear(data, to_lookup)',
	globals=globals(),
	number=10
)
print(f'Linear search takes {baseline:.6f}s')

comparison = timeit.timeit(
	stmt='run_bisect(data, to_lookup)',
	globals=globals(),
	number=10
)
print(f'Bisect search take {comparison:.6f}s')

slowdown = 1 + (baseline - comparison) / comparison
print(f'{slowdown:.1f}x time')
