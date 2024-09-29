import sys
import os
# To access to my module or use a virtual env and comment the line below
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cryptage.crypting import *

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
