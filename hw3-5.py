score = list(map(int, input().split()))

def find_max(x):
    if len(x) > 5:
        half_idx = int(len(x)/2)
        include = x[half_idx] + find_max(x[:half_idx-1]) + find_max(x[half_idx+2:])
        exclude = find_max(x[:half_idx]) + find_max(x[half_idx+1:])
        return max(include, exclude)
    else:
        if len(x) == 5:
            return max(x[0]+x[2]+x[4], x[0]+x[2], x[0]+x[3], x[0]+x[4], x[1]+x[3], x[1]+x[4], x[2]+x[4])
        elif len(x) == 4:
            return max(x[0]+x[2], x[0]+x[3], x[1]+x[3])
        elif len(x) == 3:
            return max(x[1], x[0]+x[2])
        elif len(x) <= 2:
            return max(x)

print(find_max(score))