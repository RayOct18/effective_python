# greatest common divisor (gcd)

def gcd(pair):
	a, b = pair
	low = min(a, b)
	for i in range(low, 0, -1):
		if a % i == 0 and b % i == 0:
			return i
	assert False, 'Not readhable'

import time

NUMBERS = [
	(1963309, 2265973), (2030677, 3814172),
	(1551645, 2229620), (2039045, 2020802),
	(1823712, 1924928), (2293129, 1020491),
	(1281238, 2273782), (3823812, 4237281),
	(3812741, 4729139), (1292391, 2123811)
]

def main():
	start = time.time()
	results = list(map(gcd, NUMBERS))
	end = time.time()

	print(results)
	print(f'Took {(end - start):.3f} seconds')

if __name__ == '__main__':
	main()
