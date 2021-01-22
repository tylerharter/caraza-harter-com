# OOP 1: Intro to Object Oriented Programming

## 1. Binary Search

### Watch: [10-minute video](https://youtu.be/hdT9W9KvuSc)

### Practice

Copy+paste the following example from the lecture (note the added
debug prints that show how the range of the list under consideration
is repeatedly cut in half):

```python
# assume L is already sorted, N=len(L)
def binary_search(L, target):
    print(target)
    left_idx = 0 # inclusive
    right_idx = len(L) # exclusive
    while right_idx - left_idx > 1:
        mid_idx = (right_idx + left_idx) // 2
        mid = L[mid_idx]
        if target >= mid:
            left_idx = mid_idx
        else:
            right_idx = mid_idx
        print(L[left_idx:right_idx])

    return right_idx > left_idx and L[left_idx] == target

print(binary_search([1,5,8,9,11,25,27,99], 27))
```

Now, make various tweaks to the example to understand how `binary_search` works in different cases:

1. what if there are an odd number of items in the list?
2. what if the same number is repeated multiple times (consecutively)
3. what if the items in the list are not in ascending order?  `binary_search` won't always return the correct answer in this case -- it only works when the list is pre-sorted.  See if you can construct an example where `binary_search` returns False when non-sorted list containing the target is passed in.

## 2. Object Oriented Programming

### Watch: [24-minute video](https://youtu.be/qvXOeZi6kbM)

### Explore

Copy, paste, and run the example from lecture:

```python
class Dog:
    def speak(dog):
        if dog.age < 2:
            print(dog.name, "bark! " * 5)
        elif dog.age > 10:
            print(dog.name, "grrrr")
        else:
            print(dog.name, "bark")

# NOT GREAT
def init(dog, name, age):
    dog.name = name
    dog.age = age
        
class Cat:
    def speak(cat):
        print("meow")

dog1 = Dog()
init(dog1, "Fido", 1)
dog2 = Dog()
init(dog2, "Sam", 12)
c1 = Cat()

# BAD
Dog.speak(dog1)

Cat.speak(dog1) # dogs don't say "meow"!!!
```

When we run the Cat version of speak on a dog, the dog says something
unexpected.  Switch it: what happens when you call the Dog version of
speak on a cat object (like `c1`)?

## 3. Methods

### Watch: [16-minute video](https://youtu.be/OArnWodKmSY)
