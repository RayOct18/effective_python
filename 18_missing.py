

def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except:
        print(f'Failed to open path {profile_path}')
        raise

class Picture(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

if __name__ == '__main__':
    path = 'test'
    picture = Picture()
    handle = picture[path]
    handle.seek(0)
    data = handle.read()
    print(data)