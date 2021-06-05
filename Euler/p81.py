import heapq


# A lot taken from: https://www.redblobgames.com/pathfinding/a-star/introduction.html


class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]
        

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Точка: x={self.x}, y={self.y}'

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    # PriorityQueue really wants it to be comparable
    def __lt__(self, other):
        return 0


class Matrix:
    def __init__(self):
        self.data = []
        with open('p081_matrix.txt') as f:
            for line in f.readlines():
                self.data.append([int(value) for value in line.split(',')])

    @property
    def width(self):
        return len(self.data[0]) if self.data else 0

    @property
    def height(self):
        return len(self.data)

    def get(self, point):
        return self.data[point.y][point.x]

    def neighbors(self, point):
        neighbors = []

        if point.x < self.width - 1:
            neighbors.append(Point(point.x + 1, point.y))
            
        if point.y < self.height - 1:
            neighbors.append(Point(point.x, point.y + 1))

        return neighbors

    def find_path(self, start, end):
        frontier = PriorityQueue()
        frontier.put(start, self.get(start))
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = self.get(start)

        while not frontier.empty():
            current = frontier.get()

            if current == end:
                break
            
            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + self.get(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)
                    came_from[next] = current

        path = [end]
        while path[-1] != start:
            path.append(came_from[path[-1]])
        path.reverse()

        return path, cost_so_far[end]

    def print_path(self, path):
        for y in range(self.height):
            line = ''
            for x in range(self.width):
                point = Point(x, y)
                if point in path:
                    line += 'x'
                else:
                    line += '.'
            print(line)



MATRIX = Matrix()
START = Point(0, 0)
END = Point(79, 79)

path, cost = MATRIX.find_path(START, END)
MATRIX.print_path(path)
print(cost)