def safe_division(numerator, denominator, /,
                  ndigits=10, *,
                  ignore_overflow=False,
                  ignore_zero_division=False):
    try:
        return round(numerator / denominator, ndigits)
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

if __name__ == '__main__':
    print(safe_division(22, 7))
    print(safe_division(22, denominator=0, ndigits=10, ignore_zero_division=True))