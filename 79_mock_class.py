class ZooDatabase:

	def get_animals(self, species):
		pass

	def get_food_period(self, species):
		pass

	def feed_animal(self, name, when):
		pass

from datetime import datetime

def do_rounds(database, species, *, utcnow=datetime.utcnow):
	now = utcnow()
	feeding_timedelta = database.get_food_period(species)
	animals = database.get_animals(species)
	fed = 0
	for name, last_mealtime in animals:
		if (now - last_mealtime) >= feeding_timedelta:
			database.feed_animal(name, now)
			fed += 1
	return fed


from unittest.mock import Mock

database = Mock(spec=ZooDatabase)
print(database.feed_animal)
database.feed_animal()
database.feed_animal.assert_any_call()

from datetime import timedelta
from unittest.mock import call

now_func = Mock(spec=datetime.utcnow)
now_func.return_value = datetime(2019, 6, 5, 15, 45)

database = Mock(spec=ZooDatabase)
database.get_food_period.return_value = timedelta(hours=3)
database.get_animals.return_value = [
	('A', datetime(2019, 6, 5, 11, 15)),
	('B', datetime(2019, 6, 5, 12, 30)),
	('C', datetime(2019, 6, 5, 12, 55))
]

result = do_rounds(database, 'Mee', utcnow=now_func)
assert result == 2


DATABASE = None

def get_database():
	global DATABASE
	if DATABASE is None:
		DATABASE = ZooDatabase()
	return DATABASE

def main(argv):
	database = get_database()
	species = argv[1]
	count = do_rounds(database, species)
	print(f'Fed {count} {species} (s)')
	return 0

import contextlib
import io
from unittest.mock import patch

with patch('__main__.DATABASE', spec=ZooDatabase):
	now = datetime.utcnow()

	DATABASE.get_food_period.return_value = timedelta(hours=3)
	DATABASE.get_animals.return_value = [
		('A', now - timedelta(hours=4.5)),
		('B', now - timedelta(hours=3.25)),
		('C', now - timedelta(hours=2)),
	]

	fake_stdout = io.StringIO()
	with contextlib.redirect_stdout(fake_stdout):
		main(['program name', 'Mee'])
	
	found = fake_stdout.getvalue()
	expected = 'Fed 2 Mee (s)\n'

	assert found == expected
