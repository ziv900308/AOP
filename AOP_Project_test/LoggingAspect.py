from AOP import *

@Aspect
class Logging_Aspect:
    def __init__(self):
        print("This is Aspect code...")

    @Pointcut(Joinpoint="execution", Pattern="MethodPattern", Filepath="app.py", Function="Service")
    def PointcutMethods(self):
        pass

    @Before(PointcutMethods)
    def logBefore():
        print("This is logBefore...")
        print("Calling...")
        print("Calling...")
