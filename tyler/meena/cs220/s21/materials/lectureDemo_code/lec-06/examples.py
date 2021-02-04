#Sep allows you to configure separator between the arguments
#End allows you to configure what character gets printed after 
#all arguments are printed

print("hello", "world", sep="|", end = ";\n")
print("hello", "meena", sep="^", end = "...\n")


print("*" * 4, "#" * 6, sep="||", end="<END>")
print("*" * 6, "#" * 8, sep="||", end="<END>")

print("\n", end="")

print("*" * 4, "#" * 6, sep="||", end="<END>\n")
print("*" * 6, "#" * 8, sep="||", end="<END>\n")
