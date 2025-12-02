import lib

def is_valid(id):
    id = str(id)
    l = len(id)
    if l % 2 == 1:
        return True
    return id[:l//2] != id[l//2:]

def is_valid_v2(id):
    if id < 10:
        return True
    id = str(id)
    l = len(id)
    p1 = 0
    p2 = 1
    p3 = 1

    while True:
        if id[p1] == id[p2]:
            p1 += 1
            p2 += 1
        elif p1 > 0:
            p1 = 0
            p3 = p2
        else:
            p1 = 0
            p2 += 1
            p3 = p2

        if p2 == l:
            break
    return p1 < p3 or (p1 % p3 != 0)
def p1():
    s = 0
    for i in lib.read().split(','):
        first, last = i.split('-')
        for j in range(int(first), int(last)+1):
            if is_valid(j):
                continue
            # print(j)
            s += j
    return s

def p2():
    s = 0
    for i in lib.read().split(','):
        first, last = i.split('-')
        for j in range(int(first), int(last)+1):
            if is_valid_v2(j):
                continue
            # print(j)
            s += j
    return s
    



print(p2())
