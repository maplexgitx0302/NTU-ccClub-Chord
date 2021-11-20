# https://www.geeksforgeeks.org/diameter-of-a-binary-tree/

class Node:
    def __init__(self, data):
        self.data      = data
        self.parent    = None
        self.children  = []
        self.h         = None

tree = {}
root = Node(1)
tree['1'] = root

N = int(input())
for _ in range(N-1):
    parent, child = input().split()
    node = Node(int(child))
    tree[child] = node
    node.parent = tree[parent]
    tree[parent].children.append(node)

def set_height(node):
    if node.children == []:
        node.h = [0, node.data]
    else:
        h_leaf = max([child.h for child in node.children], key=lambda x: (x[0], -x[1]))
        node.h = [h_leaf[0]+1, h_leaf[1]]

def diameter(node):
    if len(node.children) == 0:
        set_height(node)
        return [0, node.data, node.data]
    elif len(node.children) == 1:
        dmt = diameter(node.children[0])
        set_height(node)
        return max(([node.h[0], min(node.h[1], node.data), max(node.h[1], node.data)], dmt), key=lambda x: (x[0], -x[1], -x[2]))
    else:
        dmts = [diameter(child) for child in node.children]
        heights = [child.h for child in node.children]
        heights.sort(reverse=True, key=lambda x: (x[0], -x[1]))
        height_pair = [[heights[0][0]+heights[1][0]+2, min(heights[0][1], heights[1][1]), max(heights[0][1], heights[1][1])]]
        set_height(node)
        return max(height_pair + dmts, key=lambda x: (x[0], -x[1], -x[2]))

result = diameter(root)
print(f"{result[1]} {result[2]}")