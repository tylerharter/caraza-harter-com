# this returns the text of the book.
# just use it!
# (you don't need to understand how it works at this point in the semester)
def read_book():
    with open('pg420.txt') as f:
        return f.read()

def main():
    text1 = "AAAAABBCCC"
    text2 = ('A good glass in the bishop\'s hostel in the devil\'s seat ' +
             'twenty-one degrees and thirteen minutes northeast and by north ' +
             'main branch seventh limb east side ' +
             'shoot from the left eye of the death\'s-head ' +
             'a bee line from the tree through the shot fifty feet out.')
    text3 = read_book()
    tab = get_table(text1)
    print(tab)

# return a dictionary
# key: a letter
# value: what is the frequency of that letter in text
def get_table(text):
    # key: a letter
    # val: how many times it appeared
    counts = {}
    for character in text:
        if not character in counts:
            counts[character] = 0
        counts[character] += 1

    probs = {}
    for letter in counts:
        probs[letter] = counts[letter] / len(text)

    return probs

main()
