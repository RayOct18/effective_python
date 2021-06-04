
if __name__ == '__main__':
    it = (x for x in open('test.txt'))
    print(next(it))
    print(next(it))
    print(next(it))