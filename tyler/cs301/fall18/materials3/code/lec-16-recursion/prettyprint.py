def pretty_print(items, indent = 0):
    for item in items:
        if type(item) == list:
            pretty_print(item, indent+2)
        else:
            print(indent * " " + item)


my_list = ["A", ["1", "2", "3"], "B", ["4", ["i", "ii"]]]

pretty_print(my_list)

