import asyncio
from threading import Lock, Thread
from concurrent.futures import ThreadPoolExecutor

TPE = ThreadPoolExecutor()

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
def tail_file(handle, interval, write_func):
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)

	async def write_async(data):
		write_func(data)
	
	coro = tail_async(handle, interval, write_async)
	loop.run_until_complete(coro)


async def tail_async(handle, interval, write_func):
	loop = asyncio.get_event_loop()

	while not handle.closed:
		try:
			line = await loop.run_in_executor(TPE, readline, handle)
		except NoNewData:
			await asyncio.sleep(interval)
			handle.close()
		else:
			await write_func(line)


def run_threads(handles, interval, output_path):
	with open(output_path, 'wb') as output:
		lock = Lock()
		def write(data):
			with lock:
				output.write(data)
		
		threads = []
		for handle in handles:
			args = (handle, interval, write)
			thread = Thread(target=tail_file, args=args)
			thread.start()
			threads.append(thread)
		
		for thread in threads:
			thread.join()

def confirm_merge(input_paths, output_path):
	inputs_cnt = output_cnt = 0
	for f in os.listdir(input_paths):
		with open(os.path.join(input_paths, f), 'r') as fh:
			inputs_cnt += len(fh.readlines())
	with open(output_path, 'r') as fh:
		output_cnt += len(fh.readlines())
	print(inputs_cnt, output_cnt)
	assert inputs_cnt == output_cnt

import os

input_paths = 'test_inputs'
handles = [open(os.path.join(input_paths, f), 'rb') for f in os.listdir(input_paths)]
output_path = 'merge_test.txt'
run_threads(handles, 0.1, output_path)
confirm_merge(input_paths, output_path)