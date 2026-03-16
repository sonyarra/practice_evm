def power(base, exponent):
    if exponent == 0:
        return 1
    else:
        return base * power(base, exponent - 1)

base = int(input("Число: "))
exponent = int(input("Степень: "))
print("Результат:", power(base, exponent))
