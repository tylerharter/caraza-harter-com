p1_name = "alice"
p2_name = "bob"
p1_points = 10
p2_points = 8

# pad names so they are 7 chars long
p1_name += " " * (7-len(p1_name))
p2_name += " " * (7-len(p2_name))

print(p1_name + "|" * p1_points)
print(p2_name + "|" * p2_points)
