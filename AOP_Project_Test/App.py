from CalculatorService import *

"""
@aspectlib.Aspect
def Aspect_Cut(*args, **kwargs):
    input("This is aop before!!")
    yield aspectlib.Proceed
    input("This is aop after!!")
"""

def main():
    calculatorService = CalculatorService()

    num1 = 10
    num2 = 5

    print("Addition:", calculatorService.add(num1, num2))
    print("Subtraction:", calculatorService.subtract(num1, num2))
    print("Multiplication:", calculatorService.multiply(num1, num2))
    print("Negation:", calculatorService.neg(num1))

    try:
        print("Division:", calculatorService.divide(num1, num2))
        print("Division by zero:", calculatorService.divide(num1, 0))
    except:
        print("Error!")

#if __name__ == "__main__":
#    aspectlib.weave(print, Aspect_Cut)
#    main()

"""
problem:
1. Around problem
2. package path problem


python parser package
AOP exclusion pointcut
python on microservice
"""