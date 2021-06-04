from collections import defaultdict

class CountMissing:
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

if __name__ == '__main__':
    increments = [('blue', 3), ('yellow', 7)]
    current = {'red': 5, 'green': 9}
    counter = CountMissing()
    result = defaultdict(counter, current)
    for key, amount in increments:
        result[key] += amount
    
    print(result)
    print(counter.added)