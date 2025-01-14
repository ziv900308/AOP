import os
from ScanAspect import *

if __name__ == '__main__':

    # print weaver target (parameter 1)
    # print("Sys.argv: ", sys.argv)
    # print("Target directory: ", os.getcwd() + "\\" + sys.argv[1])

    analyzer = DecoratorAnalyzer()
    aspect_files = analyzer.scan_aspect_decorator()

    if aspect_files == []:
        print("Aspect file not found...")
    else:
        for aspect_file in aspect_files:
            print("=================================== Aspect file ===================================")
            print(aspect_file)

            f = os.popen(f'python {aspect_file}', 'r')
            print(f.read())
            f.close()