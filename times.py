import re
time = 0
test = input(">>> ")
for type in [['s', 'seconds', 1], ['m', 'minutes', 60], ['h', 'hours', 3600], ['d', 'days', 86400]]:
    if type[0] in list(test):
        time += int(re.findall(f'(\d+){type[0]}', test)[0]) * type[2]

print(time)
        