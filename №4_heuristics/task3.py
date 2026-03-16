def main():
    graph = {}
    
    cities = input("Введите города через пробел: ").split()
    
    for city in cities:
        graph[city] = []
    
    print("Введите возможные пути в город (формат: Город = откуда можно приехать):")
    print("(Для окончания ввода оставьте строку пустой)")
    
    while True:
        line = input().strip()
        if not line:
            break
        
        if '=' in line:
            target, sources = line.split('=')
            target = target.strip()
            sources = sources.strip().split()
            if target in graph:
                graph[target].extend(sources)
    
    start = 'А'
    end = 'И'
    through = 'В'
    
    paths_A_to_B = find_paths(graph, start, through)
    
    paths_B_to_I = find_paths(graph, through, end)
    
    total_paths = len(paths_A_to_B) * len(paths_B_to_I)
    
    print(f"Всего путей: {total_paths}")


def find_paths(graph, start, end):
    result = []
    
    def dfs(current, path):
        if current == end:
            result.append(path[:])
            return
        for city in graph:
            if current in graph[city] and city not in path:
                dfs(city, path + [city])
    
    dfs(start, [start])
    return result


if __name__ == "__main__":
    main()