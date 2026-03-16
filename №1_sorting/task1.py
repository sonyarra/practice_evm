def bubble_sort(arr):
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        for j in range(n - 1 - i):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

    return comparisons, swaps

def main():
    input_str = input("Введите массив целых чисел через пробел: ")
    arr = list(map(int, input_str.split()))

    print("Исходный массив:", ' '.join(map(str, arr)))

    comp, swaps = bubble_sort(arr)

    print("Отсортированный массив:", ' '.join(map(str, arr)))
    print("Количество сравнений:", comp)
    print("Количество обменов:", swaps)


if __name__ == "__main__":
    main()