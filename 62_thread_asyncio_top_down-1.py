

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
	while not handle.closed:
		try:
			line = readline(handle)
		except NoNewData:
			time.sleep(interval)
			handle.close()
		else:
			write_func(line)

from threading import Lock, Thread
import asyncio

async def run_tasks_mixed(handles, interval, output_path):
	loop = asyncio.get_event_loop()

	with open(output_path, 'wb') as output:
		async def write_async(data):
			output.write(data)
			output.flush()

		def write(data):
			coro = write_async(data)
			future = asyncio.run_coroutine_threadsafe(coro, loop)
			future.result()
		
		tasks = []
		for handle in handles:
			task = loop.run_in_executor(None, tail_file, handle, interval, write)
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
asyncio.run(run_tasks_mixed(handles, 0.1, output_path))
confirm_merge(input_paths, output_path)