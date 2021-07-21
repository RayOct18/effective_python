from threading import Thread

class WriteThread(Thread):
	def __init__(self, output_path):
		super().__init__()
		self.output_path = output_path
		self.output = None
		self.loop = asyncio.new_event_loop()

	def run(self):
		asyncio.set_event_loop(self.loop)
		with open(self.output_path, 'wb') as self.output:
			self.loop.run_forever()
		self.loop.run_until_complete(asyncio.sleep(0))

	async def real_write(self, data):
		self.output.write(data)
		self.output.flush()

	async def write(self, data):
		coro = self.real_write(data)
		future = asyncio.run_coroutine_threadsafe(coro, self.loop)
		await asyncio.wrap_future(future)

	async def real_stop(self):
		self.loop.stop()
	
	async def stop(self):
		coro = self.real_stop()
		future = asyncio.run_coroutine_threadsafe(coro, self.loop)
		await asyncio.wrap_future(future)

	async def __aenter__(self):
		loop = asyncio.get_event_loop()
		await loop.run_in_executor(None, self.start)
		return self
	
	async def __aexit__(self, *_):
		await self.stop()

class NoNewData(Exception):
	pass

def readline(handle):
	offset = handle.tell()
	handle.seek(0, 2)
	length = handle.tell()

	if length == offset:
		raise NoNewData
	
	handle.seek(offset, 0)
	return handle.readline()

import time
async def tail_async(handle, interval, write_func):
	loop = asyncio.get_event_loop()

	while not handle.closed:
		try:
			line = await loop.run_in_executor(None, readline, handle)
		except NoNewData:
			await asyncio.sleep(interval)
			handle.close()
		else:
			await write_func(line)

import asyncio

async def run_fully_async(handles, interval, output_path):
	async with WriteThread(output_path) as output:
		tasks = []
		for handle in handles:
			coro = tail_async(handle, interval, output.write)
			task = asyncio.create_task(coro)
			tasks.append(task)
		await asyncio.gather(*tasks)

def confirm_merge(input_paths, output_path):
	inputs_cnt = output_cnt = 0
	for f in os.listdir(input_paths):
		with open(os.path.join(input_paths, f), 'r') as fh:
			inputs_cnt += len(fh.readlines())
	with open(output_path, 'r') as fh:
		output_cnt += len(fh.readlines())
	assert inputs_cnt == output_cnt
	print(inputs_cnt, output_cnt)

import os

input_paths = 'test_inputs'
handles = [open(os.path.join(input_paths, f), 'rb') for f in os.listdir(input_paths)]
output_path = 'merge_test.txt'
asyncio.run(run_fully_async(handles, 0.1, output_path))
confirm_merge(input_paths, output_path)
