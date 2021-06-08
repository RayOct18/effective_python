

class LazyRecord:
    def __init__(self):
        self.exists = 5
    
    def __getattr__(self, name):
        value = f'Value for {name}'
        setattr(self, name, value)
        return value


class LoggingLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(f'* Called __getattr__({name}), '
              f'populating instance dictionary.')
        result = super().__getattr__(name)
        print(f'* Returning {result}')
        return result


class ValidatingRecord:
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name})')
        try:
            value = super().__getattribute__(name)
            print(f'* Found {name}, returning {value}')
            return value
        except AttributeError:
            value = f'Value for {name}'
            print(f'* Setting {name} to {value}')
            setattr(self, name, value)
            return value


class SavingRecord:
    def __init__(self):
        pass
    def __setattr__(self, name, value):
        super().__setattr__(name, value)


class DictionaryRecord:
    def __init__(self, data):
        self._data = data
    
    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name})')
        data_dict = super().__getattribute__('_data')
        return data_dict


if __name__ == '__main__':
    # data = LazyRecord()
    # data = LoggingLazyRecord()
    # data = ValidatingRecord()
    data = DictionaryRecord({'foo': 3})
    print('Before: ', data.__dict__)
    print('1st foo: ', data.foo)
    print('2nd foo: ', data.foo)
    print('exist: ', data.exists)
    print('After: ', data.__dict__)

    data = SavingRecord()
    print(data.__dict__)
    data.foo = 18
    print(data.__dict__)
    data.foo = 1
    print(data.__dict__)