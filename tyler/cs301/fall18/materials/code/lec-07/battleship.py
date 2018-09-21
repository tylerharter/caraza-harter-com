goal_x = 3
goal_y = 4

x = int(input("please enter x: "))
y = int(input("please enter y: "))

normal_line = '-' * 10 + '\n'
print(normal_line * y, end='')
print('-' * x + '!' + '-' * (9 - x))
print(normal_line * (9 - y))

hit = x == goal_x and y == goal_y
print('Hit? ' + str(hit))