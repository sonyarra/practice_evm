def sum_digits(n):
    if n == 0:
        return 0
    else:
        return n % 10 + sum_digits(n // 10)

num = int(input("Число: "))
print("Сумма цифр:", sum_digits(num))
