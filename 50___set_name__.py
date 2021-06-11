

class Field:
	def __init__(self):
		self.name = None
		self.internal_name = None

	def __set_name__(self, owner, name):
		self.name = name
		self.internal_name = '_' + name

	def __get__(self, instance, instance_type):
		if instance is None:
			return self
		return getattr(instance, self.internal_name, '')
	
	def __set__(self, instance, value):
		setattr(instance, self.internal_name, value)


class FixedCustomer:
	fisrt_name = Field()
	last_name = Field()


class Customer:
	def __getattr__(self, name):
		setattr(self, name, None)


if __name__ == '__main__':

	cust = Customer()
	print('Before: ', cust.fisrt_name, cust.__dict__)
	cust.fisrt_name = 'John'
	print('After: ', cust.fisrt_name, cust.__dict__)
	print('Deny: ', cust.miss, cust.__dict__)

	# pre-define the row index
	cust = FixedCustomer()
	print('Before: ', cust.fisrt_name, cust.__dict__)
	cust.fisrt_name = 'John'
	print('After: ', cust.fisrt_name, cust.__dict__)
	print('Deny: ', cust.miss, cust.__dict__)
