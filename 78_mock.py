from datetime import datetime, timedelta
from unittest.mock import Mock


def get_food_period(database, species):
	pass

def feed_animal(databse, name, when):
	pass

def get_animals(database, species):
	pass


def do_rounds_mock(database, species, *,
			  now_func=datetime.utcnow,
			  food_func=get_food_period,
			  animals_func=get_animals,
			  feed_func=feed_animal):
	now = now_func()
	feeding_timedelta = food_func(database, species)
	animals = animals_func(database, species)
	fed = 0

	for name, last_mealtime in animals:
		if (now - last_mealtime) > feeding_timedelta:
			feed_func(database, name, now)
			fed += 1
	return fed

def do_rounds(database, species, *, utcnow=datetime.utcnow):
	now = utcnow()
	feeding_timedelta = get_food_period(database, species)
	animals = get_animals(database, species)
	fed = 0

	for name, last_mealtime in animals:
		if (now - last_mealtime) > feeding_timedelta:
			feed_animal(database, name, now)
			fed += 1
	return fed

now_func = Mock(spec=datetime.utcnow)
now_func.return_value = datetime(2019, 7, 3, 15, 45)

food_func = Mock(spec=get_food_period)
food_func.return_value = timedelta(hours=3)

animals_func = Mock(spec=get_animals)
animals_func.return_value = [
	('A', datetime(2019, 7, 3, 11, 4)),
	('B', datetime(2019, 7, 3, 12, 4)),
	('C', datetime(2019, 7, 3, 12, 45)),
]

feed_func = Mock(spec=feed_animal)

database = object()
result = do_rounds_mock(database, 'Mee',
				   now_func=now_func,
				   food_func=food_func,
				   animals_func=animals_func,
				   feed_func=feed_func)

assert result == 2

from unittest.mock import call

food_func.assert_called_once_with(database, 'Mee')
animals_func.assert_called_once_with(database, 'Mee')
feed_func.assert_has_calls(
	[
		call(database, 'A', now_func.return_value),
		call(database, 'B', now_func.return_value),
	],
	any_order=True
)


from unittest.mock import patch

print('Outside patch: ', get_animals)
with patch('__main__.get_animals'):
	print('Inside patch: ', get_animals)

fake_now = datetime(2019, 1, 2, 3, 4)
try:
	with patch('datetime.datetime.utcnow'):
		datetime.utcnow.return_value = fake_now
except TypeError as e:
	print(e)

def get_do_rounds_time():
	return datetime.utcnow()

with patch('__main__.get_do_rounds_time'):
	print(get_do_rounds_time)


from unittest.mock import DEFAULT

with patch.multiple('__main__',
					 autospec=True,
					 get_food_period=DEFAULT,
					 get_animals=DEFAULT,
					 feed_animal=DEFAULT):
	now_func = Mock(spec=datetime.utcnow)
	now_func.return_value = datetime(2019, 7, 3, 15, 45)
	get_food_period.return_value = timedelta(hours=3)
	get_animals.return_value = [
		('A', datetime(2019, 7, 3, 11, 4)),
		('B', datetime(2019, 7, 3, 12, 4)),
		('C', datetime(2019, 7, 3, 12, 45)),
	]

	result = do_rounds(database, 'Mee', utcnow=now_func)
	assert result == 2

	get_food_period.assert_called_once_with(database, 'Mee')
	get_animals.assert_called_once_with(database, 'Mee')
	feed_animal.assert_has_calls(
		[
			call(database, 'A', now_func.return_value),
			call(database, 'B', now_func.return_value),
		],
		any_order=True
	)