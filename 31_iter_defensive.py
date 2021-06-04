from collections import Iterator

class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path
    
    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


if __name__ == '__main__':
    visits = ReadVisits('./test.txt')
    print(normalize_defensive(visits))

    visits = [10, 23, 255, 67]
    print(normalize_defensive(visits))

    visits = ReadVisits('./test.txt')
    print(normalize_defensive(iter(visits))