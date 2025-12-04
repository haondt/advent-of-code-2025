import lib

def p1():
    grid = lib.Grid.from_string(lib.read())

    s = 0
    for point, cell in grid.enumerate():
        if cell == '.':
            continue
        adjacent_rolls = sum([1 for d in lib.ALL_DIRECTIONS if grid.cell(point + d) == '@'])
        if adjacent_rolls < 4:
            s += 1
    return s

def remove_roll_if_possible(grid, point) -> int:
    cell = grid[point]
    if cell != '@':
        return 0
    adjacent_rolls = [point + d for d in lib.ALL_DIRECTIONS if grid.cell(point + d) == '@']
    if len(adjacent_rolls) >= 4:
        return 0

    grid[point] = 'x'
    s = 1
    for p in adjacent_rolls:
        s += remove_roll_if_possible(grid, p)
    return s


def p2():
    grid = lib.Grid.from_string(lib.read())

    s = 0
    for point, cell in grid.enumerate():
        s += remove_roll_if_possible(grid, point)

    return s

print(p2())
