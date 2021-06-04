from functools import wraps

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args}, {kwargs})')
        print(f'{result}')
        return result
    return wrapper

@trace
def println(str1, str2, str3=None, str4=None):
    print(str1)
    print(str2)
    print(str3)
    print(str4)
    return (str1, str2, str3, str4)

if __name__ == '__main__':
    println('Hello', 'World', str3='Bye', str4='World')
    print(println)