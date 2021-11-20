n     = int(input())

l, r, h = list(map(int, input().split()))
point = []

temp  = [[r, h]]
x, y  = l, 0

def temp_sort():
    global temp
    temp.sort(key=lambda rect: (-rect[1], -rect[0]))
    best_r, best_h = 0, 10000
    effective_temp = []
    for i in range(len(temp)):
        if temp[i][1] < best_h and temp[i][0] > best_r:
            best_r, best_h = temp[i]
            effective_temp.append(temp[i])
    temp = effective_temp

def temp_forward(l, x, y):
    global point, temp
    temp_sort()

    # go to the top
    new_y = temp[0][1]
    if new_y != y:
        y = new_y
        point.append([x, y])

    # go downstairs
    new_temp = []
    for i in range(len(temp)):
        if x < l:
            if temp[i][0] <= l:
                new_x, new_y = temp[i][0], temp[i][1]
            else:
                new_x, new_y = l, temp[i][1]
                new_temp.append([temp[i][0], temp[i][1]])
            if y != new_y:
                point.append([x, new_y])
            x, y = new_x, new_y
        else:
            new_temp.append([temp[i][0], temp[i][1]])
    temp = new_temp
    
    # check if we go to l
    if x != l:
        point.append([x, 0])
        x, y = l, 0
    return x, y

for _ in range(n-1):
    l, r, h = list(map(int, input().split()))
    if l == x:
        temp.append([r, h])
    elif l > x:
        x, y = temp_forward(l, x, y)
        temp.append([r, h])

temp_forward(10000000, x, y)

for p in point:
    print(p[0], p[1])