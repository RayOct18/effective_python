

class EOFError(Exception):
	pass


class ConnectionBase:
	# def __init__(self, connection):
	def __init__(self, reader, writer):

		# self.connection = connection
		self.reader = reader

		# self.file = connection.makefile('rb')
		self.writer = writer
	
	# def send(self, command):
	async def send(self, command):
		line = command + '\n'
		data = line.encode()

		# self.connection.send(data)
		self.writer.write(data)
		await self.writer.drain()  # buffer flush

	# def receive(self):
	async def receive(self):

		# line = self.file.readline()
		line = await self.reader.readline()

		if not line:
			raise EOFError('Connection closed')
		return line[:-1].decode()


import random

WARMER = 'Warmer'
COLDER = 'Colder'
UNSURE = 'Unsure'
CORRECT = 'Correct'


class UnknownCommandError(Exception):
	pass


class Session(ConnectionBase):
	def __init__(self, *args):
		super().__init__(*args)
		self._clear_state(None, None)

	def _clear_state(self, lower, upper):
		self.lower = lower
		self.upper = upper
		self.secret = None
		self.guesses = []

	# def loop(self):
	async def loop(self):
		# while command := self.receive():
		while command := await self.receive():
			parts = command.split(' ')
			if parts[0] == 'PARAMS':
				self.set_params(parts)
			elif parts[0] == 'NUMBER':
				# self.send_number()
				await self.send_number()
			elif parts[0] == 'REPORT':
				self.receive_report(parts)
			else:
				raise UnknownCommandError(command)
		
	def set_params(self, parts):
		assert len(parts) == 3
		lower = int(parts[1])
		upper = int(parts[2])
		self._clear_state(lower, upper)
	
	def next_guess(self):
		if self.secret is not None:
			return self.secret
		
		while True:
			guess = random.randint(self.lower, self.upper)
			if guess not in  self.guesses:
				return guess
	
	# def send_number(self):
	async def send_number(self):
		guess = self.next_guess()
		self.guesses.append(guess)
		# self.send(format(guess))
		await self.send(format(guess))
	
	def receive_report(self, parts):
		assert len(parts) == 2
		decision = parts[1]

		last = self.guesses[-1]
		if decision == CORRECT:
			self.secret = last
		
		print(f'Server: {last} is {decision}')


import contextlib
import math


class Client(ConnectionBase):
	def __init__(self, *args):
		super().__init__(*args)
		self._clear_state()

	def _clear_state(self):
		self.secret = None
		self.last_distance = None

	#  contextlib example, https://www.liaoxuefeng.com/wiki/1016959663602400/1115615597164000
	# @contextlib.contextmanager
	# def session(self, lower ,upper, secret):
	@contextlib.asynccontextmanager
	async def session(self, lower ,upper, secret):
		print(f'Guess a number between {lower} and {upper}!'
			f'shhhh, it is {secret}.')
		self.secret = secret
		# self.send(f'PARAMS {lower} {upper}')
		await self.send(f'PARAMS {lower} {upper}')
		try:
			yield
		finally:
			self._clear_state()
			# self.send('PARAMS 0 -1')
			await self.send('PARAMS 0 -1')
	
	# def request_numbers(self, count):
	async def request_numbers(self, count):
		for _ in range(count):
			# self.send('NUMBER')
			await self.send('NUMBER')
			# data = self.receive()
			data = await self.receive()
			yield int(data)
			if self.last_distance == 0:
				return

	# def report_outcome(self, number):
	async def report_outcome(self, number):
		new_distance = math.fabs(number - self.secret)
		decision = UNSURE

		if new_distance == 0:
			decision = CORRECT
		elif self.last_distance is None:
			pass
		elif new_distance < self.last_distance:
			decision = WARMER
		elif new_distance > self.last_distance:
			decision = COLDER
		
		self.last_distance = new_distance
		# self.send(f'REPORT {decision}')
		await self.send(f'REPORT {decision}')
		return decision


import socket
# from threading import Thread
import asyncio

# def handle_connection(connection):
	# with connection:
	# 	session = Session(connection)
	# 	try:
	# 		session.loop()
	# 	except EOFError:
	# 		pass
async def handle_connection(reader, writer):
	session = Session(reader, writer)
	try:
		await session.loop()
	except EOFError:
		pass

# def run_server(address):
# 	with socket.socket() as listener:
# 		listener.bind(address)
# 		listener.listen()
# 		while True:
# 			connection, _ = listener.accept()
# 			thread = Thread(target=handle_connection,
# 							args=(connection,),
# 							daemon=True)
# 			thread.start()
async def run_server(address):
	server = await asyncio.start_server(handle_connection, *address)
	async with server:
		await server.serve_forever()

# def run_client(address):
# 	with socket.create_connection(address) as connection:
# 		client = Client(connection)
# 		with client.session(1, 5, 3):
# 			results = [(x, client.report_outcome(x)) for x in client.request_numbers(5)]

# 		with client.session(10, 15, 12):
# 			for number in client.request_numbers(5):
# 				outcome = client.report_outcome(number)
# 				results.append((number, outcome))
# 		return results
async def run_client(address):
	streams = await asyncio.open_connection(*address)
	client = Client(*streams)

	async with client.session(1, 5, 3):
		results = [(x, await client.report_outcome(x)) async for x in client.request_numbers(5)]

	async with client.session(10, 15, 12):
		async for number in client.request_numbers(5):
			outcome = await client.report_outcome(number)
			results.append((number, outcome))
	_, writer = streams
	writer.close()
	await writer.wait_closed()

	return results

# def main():
# 	address = ('127.0.0.1', 1234)
# 	server_thread = Thread(target=run_server,
# 						   args=(address,),
# 						   daemon=True)
# 	server_thread.start()

# 	results = run_client(address)
# 	for number, outcome in results:
# 		print(f'Client: {number} is {outcome}')
async def main():
	address = ('127.0.0.1', 4321)
	server = run_server(address)
	asyncio.create_task(server)

	results = await run_client(address)
	for number, outcome in results:
		print(f'Client: {number} is {outcome}')

asyncio.run(main())
