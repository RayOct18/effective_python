from heapq import heappush, heappop
import functools

@functools.total_ordering  # give a comparison method, this class decorator supplies the rest.
class Book:
	def __init__(self, title, due_date):
		self.title = title
		self.due_date = due_date
		self.returned = False # for returned early

	def __lt__(self, other):
		return self.due_date < other.due_date

def add_book(queue, book):
	heappush(queue, book)

queue = []
add_book(queue, Book('A','2019-04-14'))
add_book(queue, Book('B','2019-06-15'))
add_book(queue, Book('C','2019-08-16'))
add_book(queue, Book('D','2019-12-17'))

class NoOverdueBooks(Exception):
	pass

def next_overdue_book(queue, now):
	while queue:
		book = queue[0]
		if book.returned:
			heappop(queue)
			continue

		if book.due_date < now:
			heappop(queue)
			return book
	
	raise NoOverdueBooks

now = '2019-06-10'

try:
	found = next_overdue_book(queue, now)
	print(found.title)

except NoOverdueBooks as e:
	pass

def return_book(queue, book):
	book.returned = True

queue = []
book = Book('A', '2019-06-04')
add_book(queue, book)
print('Before return: ', [x.title for x in queue])
return_book(queue, book)
print('After return: ', [x.title for x in queue])


import random
import timeit

def print_results(count, tests):
	avg_iteration = sum(tests) / len(tests)
	print(f'Count {count:>5,} tasks {avg_iteration:.6f}s')
	return count, avg_iteration

def print_delta(before, after):
	before_count, before_time = before
	after_count, after_time = after
	growth = 1 + (after_count - before_count) / before_count
	slowdown = 1 + (after_time - before_time) / before_time
	print(f'{growth:>4.1f}x data size, {slowdown:>4.1f}x time')

def list_overdue_benchmark(count):
	def prepare():
		to_add = list(range(count))
		random.shuffle(to_add)
		return [], to_add
	
	def run(queue, to_add):
		for i in to_add:
			heappush(queue, i)
		
		while queue:
			heappop(queue)

	tests = timeit.repeat(
		setup='queue, to_add = prepare()',
		stmt='run(queue, to_add)',
		globals=locals(),
		repeat=100,
		number=1
	)
	return print_results(count, tests)

baseline = list_overdue_benchmark(500)
for count in (1_000, 1_500, 2_000, 3_000):
	comparison = list_overdue_benchmark(count)
	print_delta(baseline, comparison)