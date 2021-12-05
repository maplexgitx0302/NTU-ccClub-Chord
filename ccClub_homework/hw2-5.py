n, m = map(int, input().split())
cell = [list(map(int, input().split())) for _ in range(n)]
virus = int(input())

infection = [[False for _ in range(m)] for _ in range(n)]

def infect(r, c):
    cell[r][c] = virus & cell[r][c]
    infection[r][c] = True
    surrounding = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
    for i, j in surrounding:
        if i>=0 and j>=0 and i<n and j<m:
            if infection[i][j] == False and cell[i][j] != -1:
                infect(i, j)

for i in range(n):
    for j in range(m):
        if cell[i][j] == virus and infection[i][j] == False:
            infect(i, j)

for i in range(n):
    for j in range(m):
        if j == m-1:
            print(cell[i][j])
        else:
            print(cell[i][j], end=' ')