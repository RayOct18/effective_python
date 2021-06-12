import subprocess
import time


def popen():
    proc = subprocess.Popen(['sleep', '1'])
    while proc.poll() is None:
        time.sleep(0.1)
        print('Working...', proc.poll())

    print('Exit status', proc.poll())


def subprocess_run():
    result = subprocess.run(
        ['echo', 'Hello from the child!'],
        capture_output=True,
        encoding='utf-8'
    )

    result.check_returncode()
    print(result)
    print(result.stdout)


def multi_popen():
    start = time.time()
    sleep_procs = []
    for _ in range(10):
        proc = subprocess.Popen(['echo', '1'])
        sleep_procs.append(proc)

    # wait these process finish
    for proc in sleep_procs:
        proc.communicate()

    end = time.time()
    delta = end - start
    print(f'Finished in {delta:.3} seconds')


if __name__ == '__main__':
    popen()
    print('=' * 20)
    subprocess_run()
    print('=' * 20)
    multi_popen()
