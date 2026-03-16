arr = list(map(int, input("Массив: ").split()))

x = int(input("Искомое число: "))

positions = [i for i, val in enumerate(arr) if val == x]

if positions:
    print("Элемент найден на позициях:", *positions)
else:
    print("Элемент отсутствует")
