numbers = input().split(',')
max_len = len(max(numbers, key=lambda x:len(x)))

def criterion(x):
    digits = list(x) + max_len*list(x)
    return tuple(digits)
      
numbers.sort(reverse=True, key=criterion)
print(''.join(numbers))