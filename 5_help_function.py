from urllib.parse import parse_qs

def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default

if __name__ == '__main__':
    my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)

    print('Red:', get_first_int(my_values, 'red'))
    print('Blue:', get_first_int(my_values, 'blue'))
    print('Green:', get_first_int(my_values, 'green'))