
def multiply(func):
    def wrapper(x):
        return func(x) * 2
    return wrapper

def sum(func):
    def wrapper(x):
        return func(x) + 13
    return wrapper

"""
Aşagıdaki dekoratörler şöyle çalışır. önce fonksiyonun üstündeki
multiply daha sonra onun üstündeki sum çalışır.
böylelikle birden fazla dekoratör kullanılabilir.
"""
@sum
@multiply
def calculate(x):
    return x + 2

print(calculate(3)) # ((x + 2) * 2) + 13 = 23 

print(calculate(0)) # ((x + 2) * 2) + 13 = 17 

print(calculate(21)) # ((x + 2) * 2) + 13 = 59 