from __future__ import annotations
from collections.abc import Callable
from typing import TypeVar, Generic, Generator
import heapq
import math


T = TypeVar('T')
U = TypeVar('U')

def read() -> str:
    return '\n'.join(read_lines())

def read_lines() -> list[str]:
    lines = []
    with open('input.txt') as f:
        for line in f:
            if len(line) > 0:
                lines.append(line.strip())
    return lines

def flatten(l):
    return [i for j in l for i in j]


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self._hash = hash((self.x, self.y))

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return str(self)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Point:
        return Point(-self.x, -self.y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return other.x == self.x and other.y == self.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def integer_direction(self):
        gcd = math.gcd(self.x, self.y)
        if gcd == 1:
            return self
        return Point(self.x // gcd, self.y // gcd)

    def __hash__(self):
        return self._hash

    def __mul__(self, scalar: int) -> Point:
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int) -> Point:
        return self.__mul__(scalar)

class Grid(Generic[T]):
    def __init__(self, cells: list[list[T]]):
        self._width = len(cells[0])
        self._height = len(cells)
        self._cells: list[list[T]] = cells

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @classmethod
    def from_size(cls, width: int, height: int, default_value: Callable[[], T]):
        return cls([[default_value() for _x in range(width)] for _y in range(height)])

    @classmethod
    def from_string(cls, input: str, caster: Callable[[str], T] = lambda x: x):
        return cls([[caster(j) for j in i] for i in input.split('\n')])

    def clone(self):
        return Grid([[cell for cell in row] for row in self._cells])

    def convert(self, converter: Callable[[T], U]) -> Grid[U]:
        return Grid([[converter(cell) for cell in row] for row in self._cells])

    def invert_y(self):
        return Grid([[cell for cell in row] for row in self._cells][::-1])

    def cell(self, point: Point) -> None | T:
        if self.has_cell(point):
            return self._cells[self._height - 1 - point.y][point.x]
        return None

    def __getitem__(self, point: Point) -> T:
        cell = self.cell(point)
        if cell is None:
            raise KeyError(f"Point {point} not inside grid")
        return cell

    def __setitem__(self, point: Point, value: T):
        self._cells[self._height - 1 - point.y][point.x] = value 

    def try_set(self, point: Point, value: T) -> bool:
        if self.has_cell(point):
            self[point] = value
            return True
        return False

    def enumerate(self) -> Generator[tuple[Point, T], None, None]:
        for y in range(self._height):
            for x in range(self._width):
                yield (Point(x, y), self._cells[self._height - 1 - y][x])

    def __str__(self):
        rows = [''.join([str(cell) for cell in row]) for row in self._cells]
        return '\n'.join(rows)

    def __repr__(self):
        return str(self)

    def to_string(self, with_numbers = False):
        if with_numbers:
            rows = [f'{self._height -x - 1:3} ' + '   '.join([f'{cell}' for cell in row]) for x, row in enumerate(self._cells)]
            s = '\n'.join(rows)
            s += '\n    ' + ''.join([f'{i:<4}' for i in range(self._width)])
            return s

        return self.__str__()

    def has_cell(self, point: Point) -> bool:
        return point.y >= 0 and point.y < self._height and point.x >= 0 and point.x < self._width

    def find(self, value: T) -> Point:
        for y in range(self._height):
            for x in range(self._width):
                point = Point(x, y)
                if self.cell(point) == value:
                    return point
        raise KeyError(f"Could not find cell with value {value}")



CARDINAL_DIRECTIONS = [
    Point(1, 0),
    Point(-1, 0),
    Point(0, 1),
    Point(0, -1)
]

ALL_DIRECTIONS = [
    Point(1, 0),
    Point(-1, 0),
    Point(0, 1),
    Point(0, -1),
    Point(1, 1),
    Point(-1, -1),
    Point(-1, 1),
    Point(1, -1)
]


class Heap():
    def __init__(self, initial = []):
        self._heap = initial
        heapq.heapify(self._heap)

    def peek(self):
        if len(self._heap) == 0:
            return None
        return self._heap[0]

    def __len__(self):
        return len(self._heap)

    def pop(self):
        return heapq.heappop(self._heap)

    def push(self, value):
        return heapq.heappush(self._heap, value)

class DijkstraNode(Generic[T]):
    def __init__(self, value: T, distance: int | None = None):
        self.distance: int | None = distance
        self.closest_neighbours: dict[T, DijkstraNode[T]] = {}
        self.is_visited = False
        self.value = value

    def __lt__(self, other: DijkstraNode):
        assert self.distance != None
        assert other.distance != None
        return self.distance < other.distance

    def __eq__(self, other):
        if not isinstance(other, DijkstraNode):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return f'DijkstraNode({self.value}, {self.distance})'

class Dijkstra(Generic[T]):
    def __init__(self, 
        start: T,
        end: T,
        get_neighbours: Callable[[T], list[tuple[T, int]]]):
        self._start = DijkstraNode(start, 0)
        self._end = DijkstraNode(end)
        self._get_neighbours = get_neighbours

    def search(self, terminate_early: bool = False):
        todo_heap = Heap([self._start])
        todo_set: set[DijkstraNode] = set([self._start])
        map: dict[T, DijkstraNode[T]] = { self._start.value: self._start }

        while len(todo_heap) != 0:
            current = todo_heap.pop()
            todo_set.remove(current)
            assert current.distance is not None

            if current == self._end:
                if terminate_early:
                    return map
                continue

            for neighbour_value, distance in self._get_neighbours(current.value):
                if neighbour_value not in map:
                    map[neighbour_value] = DijkstraNode(neighbour_value)
                neighbour = map[neighbour_value]

                if neighbour.is_visited:
                    continue

                new_distance = distance + current.distance
                if neighbour.distance is None or new_distance < neighbour.distance:
                    neighbour.distance = new_distance
                    neighbour.closest_neighbours = { current.value: current }

                    if neighbour not in todo_set:
                        todo_set.add(neighbour)
                        todo_heap.push(neighbour)

                elif neighbour.distance == new_distance:
                    neighbour.closest_neighbours[current.value] = current

            current.is_visited = True
        return map
