import time
import random

def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def measure_time(sort_func, arr):
    arr_copy = arr.copy()
    start = time.perf_counter()
    sort_func(arr_copy)
    end = time.perf_counter()
    return (end - start) * 1000  

def main():
    print("Введите размер массива:")
    size = int(input())
    print("Введите элементы массива через пробел:")
    data = list(map(int, input().split()))
    if len(data) != size:
        print("Количество элементов не соответствует размеру, будет использовано", len(data))
        size = len(data)

    arr = data[:size] 

    print("\n--- Результаты для заданного массива ---")

    time_sel = measure_time(selection_sort, arr)
    sorted_arr_sel = arr.copy()
    selection_sort(sorted_arr_sel)
    print(f"Сортировка выбором: {' '.join(map(str, sorted_arr_sel))} (время: {time_sel:.3f} мс)")

    time_ins = measure_time(insertion_sort, arr)
    sorted_arr_ins = arr.copy()
    insertion_sort(sorted_arr_ins)
    print(f"Сортировка вставками: {' '.join(map(str, sorted_arr_ins))} (время: {time_ins:.3f} мс)")

    print("\n--- Сравнение времени на случайных массивах разного размера ---")
    print("Размер\tВыбор (мс)\tВставки (мс)")
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    for sz in sizes:
        test_arr = [random.randint(0, 10000) for _ in range(sz)]
        t_sel = measure_time(selection_sort, test_arr)
        t_ins = measure_time(insertion_sort, test_arr)
        print(f"{sz}\t{t_sel:.3f}\t\t{t_ins:.3f}")

if __name__ == "__main__":
    main()