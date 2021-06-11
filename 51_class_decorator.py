from functools import wraps
import types


def trace_func(func):
	if hasattr(func, 'tracing'):
		return func

	@wraps(func)
	def wrapper(*args, **kwargs):
		result = None
		try:
			result = func(*args, **kwargs)
			return result
		except Exception as e:
			result = e
			raise
		finally:
			print(f'{func.__name__}({args}, {kwargs}) -> '
			      f'{result}')
	wrapper.tracing = True
	return wrapper


trace_types = (
	types.MethodType,
	types.FunctionType,
	types.BuiltinFunctionType,
	types.BuiltinMethodType,
	types.MethodDescriptorType,
	types.ClassMethodDescriptorType
)

def trace(klass):
	for key in dir(klass):
		value = getattr(klass, key)
		if isinstance(value, trace_types):
			wrapped = trace_func(value)
			setattr(klass, key, wrapped)
	return klass

@trace
class TraceDict(dict):
	pass


if __name__ == '__main__':
	trace_dict = TraceDict([('hi', 1)])
	trace_dict['yo'] = 3
	try:
		trace_dict['no']
	except KeyError:
		pass
