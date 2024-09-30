import sys
import os
# To access to my module or use a virtual env and comment the line below
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cryptage.crypting import *

# function: decompose an integer into a sum of powers of 2
# input: int
# output: list of int
# result: list of exponents of 2 in our sum
def intToBinExp(num):
    binNum = bin(num)
    l = []
    for i in range(2,len(binNum)):
        if binNum[i] == "1":
            l.append(len(binNum) - 1 - i )
    return l

# fonction : calcculate an integer to the power of an other integer
# with the algorythm of fast exponentielle
# input : int , int list
# output : int
# result : the integer to the power of an other (with specific format : see intToBinExp )
def fastExp(c,lexp):
    res = 1
    lexp.reverse()
    for i in lexp:
         if i == 0:
            res *= c
         else:
            # (c ^ (2 ^ (i - 1))) ^ 2
            res *= (c ** (2 ** (i - 1))) ** 2
    return res

#Test function   
def testIntToBinExp():
    assert intToBinExp(129) == [7,0]
    assert intToBinExp(64) == [6]
    assert intToBinExp(34) == [5,1]
    assert intToBinExp(21) == [4,2,0]
    assert intToBinExp(0) == []
    assert intToBinExp(1) == [0]

#Run test function
testIntToBinExp()

#Test function
def testFastExp():
    assert fastExp(5,intToBinExp(9)) == 1953125
    assert fastExp(6,intToBinExp(7)) == 279936
    assert fastExp(8,intToBinExp(4)) == 4096
    assert fastExp(1,intToBinExp(0)) == 1
    assert fastExp(9,intToBinExp(12)) == 282429536481

#Run test function
testFastExp()
