# \asd\qwe/rt/
# qwer\sdf\gghj/xbb/
# abc\abc/abc\abc/abc

input_str = input()
stack = []
s = ""
output = ""

for i in range(len(input_str)):
    if input_str[i] == "\\":
        stack.append(s)
        s = ""
    elif input_str[i] == "/":
        last = stack.pop()
        s = last + s[::-1]
    else:
        s += input_str[i]

print(s)