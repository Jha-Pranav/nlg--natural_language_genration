from gramex.transforms import handler
from math import factorial
from typing import List
from numpy import prod

@handler
def combinations(n:int, k:int) -> float:
    '''combinations(10, 4): ways to pick 4 objects from 10 ignoring order'''
    print(n,k)
    return factorial(n) / factorial(k) / factorial(n - k)


def total(*items):
    return sum(float(item) for item in items)

@handler
def multiply(v: List[int]):
    return prod(v)

def name_age(handler):
    print(handler.path_args)
    name = handler.path_args[0]
    age = handler.path_args[1]
    return name + ' is ' + age + ' years old'

def method(handler):
    handler.set_header('Content-Type', 'application/pdf')
    handler.set_header('Content-Disposition', 'attachment; filename=download.pdf')
    return open('download.pdf', 'rb').read()
