

class Polygon:
    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.sides < 3:
            raise ValueError('Polygons need 3+ sides')


class Filled:
    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.color not in ('red', 'green', 'blue'):
            raise ValueError('Fills need a valid color')


print('Before class')
class RedTriangle(Filled, Polygon):
    color = 'red'
    sides = 3
print('After class')

print('Before class')
class Wrong(Filled, Polygon):
    color = 'yellow'
    sides = 2
print('After class')