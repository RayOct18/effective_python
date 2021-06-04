from collections import defaultdict


class Visits:
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)


if __name__ == '__main__':
    visits = Visits()
    visits.add('Taiwan', 'Taipei')
    visits.add('Taiwan', 'New Taipei City')
    print(visits.data.get('Taiwan'))
