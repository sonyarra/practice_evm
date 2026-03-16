def print_array(arr, index=0):
    if index == len(arr):
        return
    print(arr[index], end=' ')
    print_array(arr, index + 1)

arr = list(map(int, input("Массив: ").split()))
print_array(arr)
print()  # Для переноса строки после вывода
