

class MyBaseClass:
    def __init__(self, value):
        self.value = value


class TimesSeven(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7


class PlusNine(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 9

class Multiple(TimesSeven, PlusNine):
    def __init__(self, value):
        super().__init__(value)


if __name__ == '__main__':
    foo = Multiple(5)
    print('7 * (9 + 5) = 98 and is', foo.value)

    mro_str = '\n'.join(repr(cls) for cls in Multiple.mro())
    print(mro_str)