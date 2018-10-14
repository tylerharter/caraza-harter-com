# this returns the text of the book.
# just use it!
# (you don't need to understand how it works at this point in the semester)
def read_book():
    with open('pg420.txt') as f:
        return f.read()

def main():
    text = read_book()
    words = text.split()

    # key is the word, value is number of appearances
    counts = {}
    
    # TODO: loop over the words and tally up the counts!

main()
