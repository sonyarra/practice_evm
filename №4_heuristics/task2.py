capacity = int(input("Вместимость: "))

items = []
print("Введите предметы (вес и ценность):")
while True:
    line = input()
    if not line.strip():
        break
    w, v = map(int, line.split())
    items.append((w, v))

items_with_ratio = [(i+1, w, v, v/w) for i, (w, v) in enumerate(items)]

items_with_ratio.sort(key=lambda x: x[3], reverse=True)

selected = []
total_value = 0
total_weight = 0

for i, w, v, ratio in items_with_ratio:
    if total_weight + w <= capacity:
        selected.append(i)
        total_weight += w
        total_value += v

print("Выбраны предметы:", ', '.join(map(str, selected)))
print("Итоговая ценность:", total_value)
