distances = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

cities = ['A', 'B', 'C', 'D']

def nearest_neighbor(dist_matrix, start=0):
    n = len(dist_matrix)
    visited = [False] * n
    path = [start]
    visited[start] = True
    total_distance = 0
    current = start

    for _ in range(n - 1):
        nearest = None
        nearest_dist = float('inf')
        for city in range(n):
            if not visited[city] and 0 < dist_matrix[current][city] < nearest_dist:
                nearest = city
                nearest_dist = dist_matrix[current][city]
        path.append(nearest)
        visited[nearest] = True
        total_distance += nearest_dist
        current = nearest

    return path, total_distance

start_city = 0 
path, total_distance = nearest_neighbor(distances, start_city)

route = " → ".join(cities[i] for i in path)

print("Кратчайший путь из чтобы посетить все точки:")
print(route)
print("Займёт этот путь:", total_distance)
