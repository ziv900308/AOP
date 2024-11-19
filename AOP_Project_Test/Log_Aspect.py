import aspectlib
from CalculatorService import *
from App import main
import inspect

@aspectlib.Aspect
def Aspect_(*args, **kwargs):
#    for func_info in inspect.stack():
#        for line in func_info:
#            print("Function information:", line)
#        print("=====================================================================================")

    print("Hello Before!!")
    print("Trigger from function:", inspect.stack()[2][4])
    print("Before calling...")
    print("args:", args)
    print("kwargs:", kwargs)


    yield aspectlib.Proceed

    print("Hello After!!")
    print("After calling...")
    print("args:", args)
    print("kwargs:", kwargs)

aspectlib.weave(CalculatorService.__name__, Aspect_)

#print(CalculatorService.__name__)
main()

"""
Python Parser
OO 嚴謹度

1. Python not support private (No information hiddening)
2. Python support polymorphism
3. Python support inheritance (only inherit behavior, data are not automatically inherit) (Python subclass not automatically invoke the constructor of
the parent class)
4. Python support abstract method (need to import package, but difficult to use)
5. Python not support const (final), need to modify code to use const function

"實做一個AOP, 針對各個AOP的特性去做評估, 並且和其他的Package做比較"
"""

