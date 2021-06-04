

def wave_cascading(amplitude_it, steps):
    for step in range(steps):
        amplitude = next(amplitude_it)
        print(f'wave_cascading: {step}, {amplitude}')
        yield amplitude

def complex_wave_cascading(amplitude_it):
    print('----------')
    yield from wave_cascading(amplitude_it, 3)
    print('----------')
    yield from wave_cascading(amplitude_it, 4)
    print('----------')
    yield from wave_cascading(amplitude_it, 5)
    print('----------')

def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10 ,10]
    it = complex_wave_cascading(iter(amplitudes))
    for amplitude in amplitudes:
        output = next(it)
        print(f'run_cascading: {output}')

if __name__ == '__main__':
    run_cascading()