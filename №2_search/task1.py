arr = list(map(int, input("Массив: ").split()))

x = int(input("Искомое число: "))

index = -1
for i, val in enumerate(arr):
    if val == x:
        index = i
        break

if index != -1:
    print("Элемент найден на позиции:", index)
else:
    print("Элемент отсутствует")
