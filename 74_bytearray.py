

dummy_bytes_video = b'0' * 10**8

def timecode_to_index(timecode):
	time = timecode.split(':')
	miles = int(time[0]) * 60 * 60 * 1000 + \
		    int(time[1]) * 60 * 1000 + \
		    int(time[2]) * 1000 + \
		    int(time[3]) * 1000
	return miles

def request_chunk(byte_offset, size):
	return dummy_bytes_video[byte_offset: byte_offset+size]

timecode = '00:00:00:08'
size = 20 * 1024 * 1024
byte_offset = timecode_to_index(timecode)
# chunk = request_chunk(byte_offset, size)

import timeit

result = timeit.timeit(
	stmt='request_chunk(byte_offset, size)',
	globals=globals(),
	number=100
) / 100
print(f'{result:0.9f} s')

print(f'20 MB/{result:0.9f} s')
print(f'Server can take {(20/result)/1024:0.2f} GB/s')
print(f'Server can take {int(1/result)} client/s')



dummy_bytes_video = b'0' * 10**8
dummy_bytes_video = memoryview(dummy_bytes_video)
result = timeit.timeit(
	stmt='request_chunk(byte_offset, size)',
	globals=globals(),
	number=100
) / 100
print(f'{result:0.9f} s')

print(f'20 MB/{result:0.9f} s')
print(f'Server can take {(20/result)/1024:0.2f} GB/s')
print(f'Server can take {int(1/result)} client/s')

data = b'shave and haircut, two bits'
print(data)
view = memoryview(data)
print(view)

dummy_bytes_video = b'0' * 10**8
dummy_bytes_video = bytearray(dummy_bytes_video)
dummy_bytes_video = memoryview(dummy_bytes_video)
result = timeit.timeit(
	stmt='request_chunk(byte_offset, size)',
	globals=globals(),
	number=100
) / 100
print(f'{result:0.9f} s')

print(f'20 MB/{result:0.9f} s')
print(f'Server can take {(20/result)/1024:0.2f} GB/s')
print(f'Server can take {int(1/result)} client/s')