import json


s= """
dr = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}

def b(d, dist):
    border = {}
    down = set()
    x, y = 0, 0
    border[0] = {0}
    for i in range(len(d)):
        for _ in range(dist[i]):
            prev_x, prev_y = x, y
            x, y = x + dr[d[i]][0], y + dr[d[i]][1]
            if x in border:
                border[x].add(y)
            else:
                border[x] = {y}
            if prev_x < x:
                down.add((prev_x, prev_y))
            elif x < prev_x:
                down.add((x, y))
    
    counter = 0
    for i in sorted(border):
        up = False
        prev = -1
        for p in sorted(border[i]):
            if up and prev != -1:
                counter += p - prev - 1
            if (i, p) in down:
                up = not up
            prev = p
    return counter

if __name__ == '__main__':
    d, dist, code = [], [], []
    m, n, max_m, max_n = 0, 0, 0, 0
    edge = 0
    with open('input.txt', 'r') as f:
        l = f.readline()
        while l:
            l = l.split()
            d.append(l[0])
            dist.append(int(l[1]))
            edge += int(l[1])
            code.append(l[2][1:-1])
            l = f.readline()

    print(b(d, dist) + edge)
    d, dist = [], []
    for c in code:
        d.append('R' if c[-1] == '0' else 'D' if c[-1] == '1' else 'L' if c[-1] == '2' else 'U')
        dist.append(int('0x' + c[1:-1], 0))
    print(b(d, dist) + sum(dist))
"""

payload = {'message': s}
payload_json = json.dumps(payload)
print(payload_json)
