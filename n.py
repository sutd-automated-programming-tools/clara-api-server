s='''

h=3
import math 
s=math.pi
print(s*h)
def f():
    return s*h
print(f())'''
t=str.encode(s)
c=compile(t,'t','exec')
exec(c)
exec('print("hekki")')
from typing import Optional
s=Optional[str]='print("hekki")'
exec(s)