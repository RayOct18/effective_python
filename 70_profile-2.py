
def my_utility(a, b):
	c = 1
	for i in range(100):
		c += a * b

def first_func():
	for _ in range(1000):
		my_utility(4, 5)

def second_func():
	for _ in range(10):
		my_utility(1, 3)

def my_program():
	for _ in range(20):
		first_func()
		second_func()

from cProfile import Profile
profiler = Profile()
profiler.runcall(my_program)

from pstats import Stats

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()
stats.print_callers()
