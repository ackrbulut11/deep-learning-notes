
def my_decorator(func):

    def wrapper():
        print("Wrapper executed.")
        func()
        print("Wrapper executed.") 

    return wrapper


@my_decorator
def hello():
    print("hELLO, wORLD!") 

hello() 
"""
Wrapper executed.
hELLO, wORLD!
Wrapper executed. 
"""

def uppercase(func):

    def inner():
        return func().upper()
    
    return inner

@uppercase
def hey():
    return "this letters lowercase but they should seem uppercase."

print(hey())    # THIS LETTERS LOWERCASE BUT THEY SHOULD SEEM UPPERCASE.
