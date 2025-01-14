import ast
import os

def scan_dir(target_directory=os.getcwd()):
    py_files = []

    # Traversing directory and subdirectory to find .py files
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            if file.endswith('.py'):

                # Combining root and file name
                full_path = os.path.join(root, file)
                py_files.append(full_path)

    return py_files

class DecoratorVisitor(ast.NodeVisitor):
    def __init__(self):
        self.decorators = []

    def visit_ClassDef(self, node):

        # Analyzing decorator from class
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                self.decorators.append({
                    'decorator': decorator.id,
                    'decorated_item': node.name,
                    'type': 'class'
                })
        self.generic_visit(node)

    # def visit_FunctionDef(self, node):

    #     # Analyzing decorator from method
    #     for decorator in node.decorator_list:
    #         if isinstance(decorator, ast.Name):
    #             self.decorators.append({
    #                 'decorator': decorator.id,
    #                 'decorated_item': node.name,
    #                 'type': 'method'
    #             })
    #     self.generic_visit(node)

class DecoratorAnalyzer:
    def __init__(self):
        self.py_files = scan_dir()
        self.decorators = []

    def analyze(self, module_path):
        # Reading .py file
        with open(module_path, 'r', encoding='utf-8') as file:
            code = file.read()

        tree = ast.parse(code)

        # Traversing AST's nodes to find decorator function (Aspect)
        visitor = DecoratorVisitor()
        visitor.visit(tree)
        self.decorators = visitor.decorators

    def print_results(self, module_path):
        print(f"\nAnalyzing decorator in {module_path}:")
        print("=" * 50)
        for dec in self.decorators:
            if str(dec['decorator']) == 'Aspect':
                print(f"Decorator '{dec['decorator']}' uses in {dec['type']} '{dec['decorated_item']}'")
                print()
                return dec['decorated_item']

    def scan_aspect_decorator(self):
        aspect_files = []

        for py_file in self.py_files:
            print(f"=================================== Scan {py_file} ===================================")
            self.analyze(py_file)
            class_name = self.print_results(py_file)

            if class_name != None:
                print("Aspect class name: ", class_name)
                aspect_files.append(py_file)

        return aspect_files