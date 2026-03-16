students = [
    ("Иванов", "Пётр", "ИС-21"),
    ("Сидоров", "Алексей", "ИС-22"),
    ("Петров", "Иван", "ИС-21"),
]

search_last_name = input("Поиск: ")

found_students = [s for s in students if s[0] == search_last_name]

if found_students:
    print("Найден студент:")
    for s in found_students:
        print(s[0], s[1], s[2])
else:
    print("Запись отсутствует")
