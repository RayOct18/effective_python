

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value

if __name__ == '__main__':
    byte = b'hello'
    string = 'hello'
    assert isinstance(to_str(byte), str)
    assert isinstance(to_str(string), str)

    assert isinstance(to_bytes(byte), bytes)
    assert isinstance(to_bytes(string), bytes)