n = int(input())

seats = []
for _ in range(n):
  row_seats = input()
  seats.append(row_seats.split(','))
    
new_seats = []
for i in range(n):
  new_row_seat = []
  for j in range(n):
    new_row_seat.append(seats[n-1-j][i])
  new_seats.append(new_row_seat)

for i in range(n):
  print(','.join(new_seats[i]))