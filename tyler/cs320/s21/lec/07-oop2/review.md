# Review

## Questions

Consider this code, then write answers/guesses on a piece of paper to
the following questions.  We'll go over the answers in the video.

```python
class Dog:
    def init(dog):
        print("created a dog")
        dog.name = name
        dog.age = age
        
    def speak(dog, mult):
        print(dog.name + ": " + "bark!")

fido = Dog()
```

1. which one is an attribute?  `dog`, `name`, `mult`, or `fido`
2. is anything printed?  Does the code crash?

For the rest of the questions , assume `init(dog)` is replaced with `__init__(dog, name, age)` and `Dog()` is replaced with `Dog("Fido", 9)`

3. is anything printed now?  Does the code crash?

Now consider the following method calls:

```python
speak(fido, 5)            # 1
fido.speak(5)             # 2
Dog.speak(fido, 5)        # 3
type(fido).speak(fido, 5) # 4
```

4. Pair each of the following descriptions with one of the above calls:
a. type-based dispatch, bad style
b. type-based dispatch, good style
c. not type-based dispatch, but works
d. crashes

5. if we call `fido.speak(5)`, what will be passed to the `dog` parameter?

6. `dog` is special: it is the receiver, the first parameter of a method.  What is a better parameter name to use instead of `dog`?

## Watch: [10-minute video](https://youtu.be/trPU-2r21AU)