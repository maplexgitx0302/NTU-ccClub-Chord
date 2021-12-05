from collections import defaultdict

N, M, K = map(int, input().split())
P = input().split()
O = list(map(int, input().split()))

Recolor = []
for _ in range(M):
    recolor = input().split()
    Recolor.append((recolor[0], int(recolor[1])))   

class Node:
    def __init__(self, index, parent, color):
        self.index = index
        self.parent = parent
        self.color = color
        self.children = []
        self.K_colors = defaultdict(int)

number = 0
tree = {}
root = Node(index='1', parent=None, color=O[0])
second = Node(index='2', parent=root, color=O[1])
root.children.append(second)
tree['1'] = root
tree['2'] = second
if root.color == second.color:
    number += 1
root.K_colors[second.color] = 1

for i in range(N-2):
    index = str(i+3)
    parent = tree[P[i]]
    node = Node(index=index, parent=parent, color=O[i+2])
    parent.children.append(node)
    parent.K_colors[node.color] += 1
    tree[index] = node
    if parent.color == node.color:
        number += 1

for i in range(M):
    node = tree[Recolor[i][0]]
    recolor = Recolor[i][1]
    if node.color == recolor:
        print(number)
        continue

    count = 0
    if node.parent != None:
        if node.parent.color == node.color:
            count -= 1
        elif node.parent.color == recolor:
            count += 1
        node.parent.K_colors[node.color] -= 1
        node.parent.K_colors[recolor] += 1
    if node.children != []:
        count -= node.K_colors[node.color]
        count += node.K_colors[recolor]
    node.color = recolor
    number += count
    print(number)