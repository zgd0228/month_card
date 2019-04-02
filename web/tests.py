from django.test import TestCase

# Create your tests here.
def w1(func):
    def inner():
        print("before w1")
        func()
        print("after w1")
    return inner

def w2(func):
    def inner():
        print("before w2")
        func()
        print("after w2")
    return inner

@w1
@w2
def test():
    print('test')
test()