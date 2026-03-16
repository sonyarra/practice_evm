def bubble_sort_optimized(arr):
    n = len(arr)
    comparisons = 0
    swaps = 0
    passes = 0

    for i in range(n - 1):
        swapped = False
        passes += 1
        for j in range(n - 1 - i):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return comparisons, swaps, passes

def main():
    input_str = input("Введите массив целых чисел через пробел: ")
    original = list(map(int, input_str.split()))
    arr = original.copy()

    comp, swaps, passes = bubble_sort_optimized(arr)

    if swaps == 0:
        print("Массив уже отсортирован.")
        print(f"Количество проходов: {passes}")
    else:
        print("Исходный массив:", ' '.join(map(str, original)))
        print("Отсортированный массив:", ' '.join(map(str, arr)))
        print("Количество сравнений:", comp)
        print("Количество обменов:", swaps)


if __name__ == "__main__":
    main()