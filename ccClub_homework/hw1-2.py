int_input = int(input())

x = 1
result = [1]

for i in range(int_input-1):
    if x * 10 <= int_input:
        x = x * 10
    elif x % 10 == 9:
        while x % 10 == 9:
            x = x // 10
        x = x + 1
    elif x + 1 <= int_input:
        x = x + 1
    else:
        x = x // 10
        while x % 10 == 9:
            x = x // 10
        x = x + 1
    result.append(x)
          
print(result)