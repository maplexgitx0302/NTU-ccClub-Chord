x = int(input())

if x==0: print(False)
if x==1: print(True)

while x > 1:
  x /= 2
  if x == 1:
    print(True)
    break
  elif x < 1:
    print(False)
    break