

def move(period, speed):
    for _ in range(period):
        yield speed

def pause(delay):
    for _ in range(delay):
        yield 0

def render(delta):
    print(f'Delta: {delta:.1f}')

def run(func):
    for delta in func():
        render(delta)

def animate_composed():
    yield from move(3, 5.0)
    yield from pause(3)
    yield from move(2, 5.0)

if __name__ == '__main__':
    run(animate_composed)