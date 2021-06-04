def careful_divide(a: float, b: float) -> float:
    """Divides a  by b

    Raises:
        ValueError: When the inputs cannot be divided.
    """
    try:
        return a/b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')

if __name__ == '__main__':
    ans = careful_divide(1, 0)
    print(ans)