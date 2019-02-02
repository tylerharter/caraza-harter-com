name1 = "alice"
name2 = "bob"

score1 = 10
score2 = 8

bars1 = '|' * score1
bars2 = '|' * score2

line1 = name1 + ": " + bars1
line2 = name2 + ": " + bars2

print(line1)
print(line2)

name2 = "bobby"
line2 = name2 + ": " + bars2


print("change bob's name")
print(line1)
print(line2)
