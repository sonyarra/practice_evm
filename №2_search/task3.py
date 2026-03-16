arr = list(map(int, input("Массив: ").split()))

x = int(input("Искомое число: "))

def binary_search(array, target):
    left, right = 0, len(array) - 1
    while left <= right:
        mid = (left + right) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

index = binary_search(arr, x)

if index != -1:
    print("Элемент найден на позиции:", index)
else:
    print("Элемент отсутствует")
