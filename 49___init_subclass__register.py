import json


registry = {}
def register_class(target_class):
	registry[target_class.__name__] = target_class


def deserialize(data):
	params = json.loads(data)
	name = params['class']
	target_class = registry[name]
	return target_class(*params['args'])


class Serializable:
	def __init__(self, *args):
		self.args = args
	
	def serialize(self):
		return json.dumps({
			'class': self.__class__.__name__,
			'args': self.args
		})
	
	def __repr__(self):
		name = self.__class__.__name__
		args_str = ', '.join(str(x) for x in self.args)
		return f'{name}({args_str})'


class RegisteredSerializable(Serializable):
	def __init_subclass__(cls):
		super().__init_subclass__()
		register_class(cls)


class Vector1D(RegisteredSerializable):
	def __init__(self, magnitude):
		super().__init__(magnitude)
		self.magnitude = magnitude

# this cannot deserialize data back to class
class Vector1DTest(Serializable):
	def __init__(self, magnitude):
		super().__init__(magnitude)
		self.magnitude = magnitude


if __name__ == '__main__':
	before = Vector1DTest(6)
	print('Before: ', before)
	data = before.serialize()
	print('Serialized: ', data)
	print('After: ', deserialize(data))
