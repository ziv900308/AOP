from CalculatorService import *

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
