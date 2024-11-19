class CalculatorService:
    def add(self, num1, num2):
        return num1 + num2
    def subtract(self, num1, num2):
        return num1 - num2
    def multiply(self, num1, num2):
        return num1 * num2
    def divide(self, num1, num2):
        if(num2 == 0):
            return "Division by zero is not allowed!"
        return num1 / num2
    def neg(self, num):
        return num * -1

class New_(CalculatorService):
    def Edd_Judge(self, num):
        if num % 2 == 0:
            return True
        return False

    def add(self, num):
        return num + 10

def main():
    calculatorService = CalculatorService()
    calculatorService2 = New_()

    num1 = 10
    num2 = 5

    print("Addition:", calculatorService.add(num1, num2))
    print()
    print("Subtraction:", calculatorService.subtract(num1, num2))
    print()
    print("Multiplication:", calculatorService.multiply(num1, num2))
    print()
    print("Negation:", calculatorService.neg(num1))
    print()

    print("Test inheritance code...")
    print("Test inheritance code, Is this number edd:", calculatorService2.Edd_Judge(num1))
    print()
    #print("Test add:", calculatorService2.add(num1, num2))
    print("Test overwriting code...")
    print("Test overwriting code, Addition:", calculatorService2.add(num1))
    print()

    try:
        print("Division:", calculatorService.divide(num1, num2))
        print()
        print("Division by zero:", calculatorService.divide(num1, 0))
        print()
    except:
        print("Error!")

# def Test():
#     print("This is test function...")
# def main():
#     Test()