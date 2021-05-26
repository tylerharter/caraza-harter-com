# Watch (Part 2)

IFRAME

# Practice

Paste and run the following starter code for a tic-tac-toe game (fill
in the `????` parts so that player 2 places an "o" in the top right):

```python
def fill_cell(tbl, symbol, row, col):
    symbol = symbol.upper() # modify a variable
    tbl[row][col] = symbol  # modify an object

board = [
    ["_", "_", "_"],
    ["_", "_", "_"],
    ["_", "_", "_"],
]
player1 = "x"
player2 = "o"

fill_cell(board, player1, 1, 1)
fill_cell(board, player2, ????, ????)
```

When `board` (argument) gets passed to `tbl` (parameter), these two
variables will refer to the same object (a list of lists).  When we
run `tbl[row][col] = ...` using the bracket syntax, we're making
within those objects.  Add some prints to verify that the changes via
`tbl` show up when we look at `board`:

```python
for row in board:
    print("".join(row))
```

The `symbol = ...` line looks similar, but there are no brackets.  In
this case, we aren't modifying the object that `symbol` refers to.
Rather, we're telling `symbol` that it should now refer to a different
object (in this case, the new string object returned by
`symbol.upper()`).

This means that even though `player1` and `symbol` originally referred
to the string object, they end up referring to different string
objects after the assignment, so if you print `player` (try it!), you
will still see the original lower case version (same for `player2`).

# Questions About the Lecture?

Please ask below.
