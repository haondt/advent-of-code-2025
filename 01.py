import lib

def p1():
    p = 50
    s = 0
    for i in lib.read_lines():
        d, c = i[0], int(i[1:])
        dir = {'L':-1,'R':1}[d]
        for _ in range(c):
            p += dir
            if p < 0:
                p = 99
            if p > 99:
                p = 0
        if p == 0:
            s += 1

    print(s)

def p2():
    p = 50
    s = 0
    for i in lib.read_lines():
        d, c = i[0], int(i[1:])
        dir = {'L':-1,'R':1}[d]
        for _ in range(c):
            p += dir
            if p < 0:
                p = 99
            if p > 99:
                p = 0
            if p == 0:
                s += 1

    print(s)

p2()
