import lib

def p1():
    data = lib.read()
    ranges, ids = data.split('\n\n')
    int_ranges = []
    for i in ranges.splitlines():
        l, r = i.split('-')
        int_ranges.append((int(l), int(r)))
    ids = ids.splitlines()
    int_ids = [int(i) for i in ids]

    s = 0
    for i in int_ids:
        for l, r in int_ranges:
            if i >= l and i <= r:
                s += 1
                break

    return s

def merge_ranges(l1,r1,l2,r2):
    if l1 > (r2+1):
        return None
    if r1 < (l2-1):
        return None
    return (min(l1, l2), max(r1, r2))

def p2():
    data = lib.read()
    ranges, _ = data.split('\n\n')
    int_ranges = []
    for i in ranges.splitlines():
        l, r = i.split('-')
        int_ranges.append((int(l), int(r)))

    merged = True
    while merged:
        merged = False
        for i, r1 in enumerate(int_ranges):
            for j, r2 in enumerate(int_ranges[i+1:]):
                merged  = merge_ranges(r1[0], r1[1], r2[0], r2[1])
                if merged is not None:
                    int_ranges[i] = merged
                    int_ranges.pop(j+i+1)
                    merged = True
                    break
                else:
                    merged = False
            if merged:
                break
    s = 0
    for l, r in int_ranges:
        s += r-l + 1
    return s



print(p2())
