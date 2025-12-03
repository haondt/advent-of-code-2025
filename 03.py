import lib

def p1():
    s = 0
    for bank in lib.read_lines():
        first = 0
        first_i = 0
        for i, battery in enumerate(bank[:-1]):
            battery = int(battery)
            if battery > first:
                first = battery
                first_i = i

        second = max(bank[first_i+1:])

        s += int(str(first) + second)
    return s

def p2():
    s = 0
    for bank in lib.read_lines():
        joltage = ''

        remaining_batteries = 12
        previous_battery_i = -1

        while remaining_batteries > 0:
            if remaining_batteries == 1:
                tmp_bank = bank[previous_battery_i+1:]
            else:
                tmp_bank = bank[previous_battery_i+1:1-remaining_batteries]
            previous_battery_i = max(range(len(tmp_bank)), key=tmp_bank.__getitem__) + previous_battery_i + 1
            joltage += bank[previous_battery_i]
            remaining_batteries -= 1
        # print(joltage)

        s += int(joltage)

    return s

print(p2())


