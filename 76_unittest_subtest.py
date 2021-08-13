from unittest import TestCase, main

def to_str(data):
	if isinstance(data, str):
		return data
	elif isinstance(data, bytes):
		return data.decode('utf-8')
	else:
		raise TypeError('Must supply str or bytes, found: %r' % data)


class DataDrivenTestCase(TestCase):
	def test_good(self):
		good_case = [
			(b'asd', 'asd'),
			('no', b'no'),
			('other', 'other')
		]
		for value, expected in good_case:
			with self.subTest(value):
				self.assertEqual(expected, to_str(value))
	
	def test_bad(self):
		bad_case = [
			(object(), TypeError),
			(b'\xfa\xfa', UnicodeDecodeError)
		]
		for value, exception in bad_case:
			with self.subTest(value):
				with self.assertRaises(exception):
					to_str(value)

if __name__ == '__main__':
	main()