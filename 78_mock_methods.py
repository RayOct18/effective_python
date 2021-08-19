

def get_animals(database, species):
	return None

from datetime import datetime
from unittest.mock import Mock

mock = Mock(spec=get_animals)

expected = [
	('A', datetime(2018, 5, 3, 11, 5)),
	('B', datetime(2010, 6, 5, 12, 1)),
	('C', datetime(2019, 3, 4, 10, 2))
]

mock.return_value = expected

database = object()
result = mock(database, 'Mee')
assert result == expected

# validate input argument
mock.assert_called_once_with(database, 'Mee')


from unittest.mock import ANY
mock = Mock(spec=get_animals)
mock('database 1', 'Mee')
mock('database 2', 'Aee')
mock('database 3', 'Bee')
mock.assert_called_with(ANY, 'Bee')


class MyError(Exception):
	pass

mock = Mock(spec=get_animals)
mock.side_effect = MyError('[Error] Ohhhhhh')
try:
	result = mock(database, 'Mee')
except MyError as e:
	print(e)