import os
import random
from threading import Thread


class GenericInputData:
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData(GenericInputData):
    def __init__(self, path):
        self.path = path
    
    def read(self):
        with open(self.path) as f:
            return f.read()
    
    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class ListInputData(GenericInputData):
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path) as f:
            return f.read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        files = config['files']
        for name in files:
            yield cls(os.path.join(data_dir, name))

    
class GenericWorker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    
    def reduce(self, other):
        self.result += other.result


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


def write_test_files(tmpdir):
    os.makedirs(tmpdir, exist_ok=True)
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write(f'{random.randint(0, 10)}\n' * random.randint(0, 100))


if __name__ == '__main__':
    tmpdir = 'test_inputs'
    write_test_files(tmpdir)
    config = {'data_dir': tmpdir}
    result = mapreduce(LineCountWorker, PathInputData, config)
    print(f'There are {result} lines')

    config = {'data_dir': tmpdir}
    config.update({'files': ['0', '1', '2', '3']})
    result = mapreduce(LineCountWorker, ListInputData, config)
    print(f'There are {result} lines')