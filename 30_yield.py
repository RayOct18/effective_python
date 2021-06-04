
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1

if __name__ == '__main__':
    address = "Hello, how are you?"
    it = index_words_iter(address)
    print(next(it))
    print(next(it))