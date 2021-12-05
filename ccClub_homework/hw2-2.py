class Node():
    def __init__(self, data=None):
        # Do something
        self.data = data
        self.last = None
        self.next = None

# Do something
N, T  = map(int, input().split())
score = list(map(int, input().split()))

HEAD = Node(score[0])
node = HEAD
for i in range(1, N):
    new_node = Node(score[i])
    new_node.last = node
    node.next = new_node
    node = node.next
    if i == N-1:
        HEAD.last = node

def print_link(HEAD):
    node = HEAD
    while True:
        if node.next != None:
            print(node.data, end=' -> ')
        else:
            print(node.data)
            break
        node = node.next

if T >= N:
    HEAD = None
else:
    count = 0
    node = HEAD
    # print_link(HEAD)
    while count < T and node.next != None:
        if node.data < node.next.data:
            count += 1
            _last, _next = node.last, node.next
            if node == HEAD:
                HEAD = _next
                HEAD.last = _last
                node = HEAD
            else:
                _last.next = _next
                _next.last = _last
                node = _last
            # print_link(HEAD)
        else:
            node = node.next

while count < T:
    HEAD.last = HEAD.last.last
    HEAD.last.next = None
    count += 1

head = HEAD