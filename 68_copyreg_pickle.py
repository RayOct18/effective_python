


class GameState:
	def __init__(self, level=0, lives=4, points=0):
		self.level = level
		self.lives = lives
		self.points = points

def pickle_game_state(game_state):
	kwargs = game_state.__dict__
	return unpickle_game_state, (kwargs, )

def unpickle_game_state(kwargs):
	return GameState(**kwargs)

import copyreg
import pickle

copyreg.pickle(GameState, pickle_game_state)
state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

class GameState:
	def __init__(self, level=0, lives=4, points=0, magic=5):
		self.level = level
		self.lives = lives
		self.points = points
		self.magic = magic

print('Before: ', state.__dict__)
state_after = pickle.loads(serialized)
print('After: ', state_after.__dict__)


class GameState:
	def __init__(self, level=0, points=0, magic=5):
		self.level = level
		self.points = points
		self.magic = magic

try:
	pickle.loads(serialized)
except TypeError as e:
	print('Error: ', e)

def pickle_game_state(game_state):
	kwargs = game_state.__dict__
	kwargs['version'] = 2
	return unpickle_game_state, (kwargs, )

def unpickle_game_state(kwargs):
	version = kwargs.pop('version', 1)
	if version == 1:
		del kwargs['lives']
	return GameState(**kwargs)

pickle.loads(serialized)
copyreg.pickle(GameState, pickle_game_state)
print('Before: ', state.__dict__)
state_after = pickle.loads(serialized)
print('After: ', state_after.__dict__)