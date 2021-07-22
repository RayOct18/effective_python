

rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(cost)
print(round(cost, 2))


from decimal import Decimal
from decimal import ROUND_UP

rate = Decimal('1.45')
seconds = Decimal(3*60 + 42)
cost = rate * seconds / Decimal(60)
print(cost)
rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)

print(Decimal('1.45'))
print(Decimal(1.45))

print(Decimal('145'))
print(Decimal(145))

rate = Decimal('0.05')
seconds = Decimal('5')
cost = rate * seconds / Decimal(60)
print(cost)

rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)