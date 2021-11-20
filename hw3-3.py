import copy
n, l, s, d = list(map(int, input().split()))
price = [list(map(int, input().split())) for _ in range(n-1)]

def get_price(pos1, pos2):
    if pos1 != pos2:
        p_min, p_max = min(pos1, pos2), max(pos1, pos2)
        return price[p_min][p_max - p_min - 1]
    else:
        return 0

matrix = [[get_price(i,j) for j in range(n)] for i in range(n)]
original_matrix = copy.deepcopy(matrix)

for _ in range(l):
    current_matrix = copy.deepcopy(matrix)
    for i in range(n):
        for j in range(i+1,n):
            for k in range(n):
                if i != k and j != k:
                    if matrix[i][j] > current_matrix[i][k] + original_matrix[k][j]:
                        matrix[i][j] = current_matrix[i][k] + original_matrix[k][j]
                        matrix[j][i] = matrix[i][j]
print(matrix[s][d])