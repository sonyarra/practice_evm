arr = list(map(int, input("Массив: ").split()))
x = int(input("Искомое число: "))

def binary_search(array, target):
    left, right = 0, len(array) - 1
    steps = 0
    while left <= right:
        steps += 1
        mid = (left + right) // 2
        if array[mid] == target:
            return True, steps
        elif array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False, steps

found, steps = binary_search(arr, x)

if found:
    print("Элемент найден.")
else:
    print("Элемент отсутствует.")
print("Количество шагов:", steps)
