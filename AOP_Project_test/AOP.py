import ast
import autopep8
import inspect


function_setting_array = []
before_log = []
after_log = []

compile_code = ""

def set_node_lineno(node, lineno, col_offset=0):
    node.lineno = lineno
    node.col_offset = col_offset
    return node

class Pointcut_Visitor(ast.NodeVisitor):
    target_function = ""

    def set_target_function(self, target_function):
        self.target_function = target_function

    def visit_ClassDef(self, node):
        if self.target_function == node.name:
            print("=================================================== Class Information ===================================================")
            print("Node class name:", node.name)

            for class_body in node.body:
                print("Node class function name:", class_body.name)
                if class_body.name not in function_setting_array:
                    function_setting_array.append(class_body.name)

        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        if self.target_function == node.name:
            print("=================================================== Function Information ===================================================")
            print("Node function name:", node.name)
            if node.name not in function_setting_array:
                function_setting_array.append(node.name)

        ast.NodeVisitor.generic_visit(self, node)

class Aspect_Visitor(ast.NodeVisitor):
    pointcut_define = ""

    def set_target(self, pointcut_define):
        print("Setting Aspect_Visitor target...")
        self.pointcut_define = pointcut_define

    def visit_FunctionDef(self, node):
        print("=================================================== Aspect Function Information ===================================================")
        print("Node args: ", len(node.args.args))
        for node_info in node.body:
            print("Node Information: ", node_info)
            if type(node_info) == ast.Expr and (before_log == [] or after_log == []):
                print()
                print("Function information: ", ast.dump(node_info.value, indent=4))
                print()
                print("AST Information: ", ast.dump(node_info, indent=4))
                print()

                if len(node.args.args) > 0:
                    ast_args = []
                    for i in range(len(node.args.args)):
                        ast_args.append(ast.Constant(value=node.name))
                    aspect_ast = ast.Expr(
                        value=ast.Call(
                            func=ast.Name(id=node.name, ctx=ast.Load()),
                            args=ast_args,
                            keywords=[]
                        )
                    )
                else:
                    aspect_ast = ast.Expr(
                        value=ast.Call(
                            func=ast.Name(id=node.name, ctx=ast.Load()),
                            args=[],
                            keywords=[]
                        )
                    )

                print("Aspect AST....", ast.dump(aspect_ast, indent=4))
                print()

                if self.pointcut_define == "Before":
                    before_log.append(set_node_lineno(aspect_ast, node.lineno))
                elif self.pointcut_define == "After":
                    after_log.append(set_node_lineno(aspect_ast, node.lineno))

        ast.NodeVisitor.generic_visit(self, node)

class AOPTransformer(ast.NodeTransformer):
    target_class = ""
    target_function = ""
    pointcut_define = ""

    def set_target(self, target_class, target_function, pointcut_define):
        print("Setting target...")
        self.target_class = target_class
        self.target_function = target_function
        self.pointcut_define = pointcut_define

    def visit_ClassDef(self, node):
        print("Target class: " + self.target_class)
        if self.target_class == node.name:
            print("Find...")
            for class_function in node.body:
                print("Class node function...", class_function.name)
                for target in self.target_function:
                    if class_function.name == target:
                        # # 在函數的開頭插入前置日誌 (TODO insert Before & After)
                        if self.pointcut_define == "Before":
                            class_function.body.insert(0, before_log[0])


                        # # 在函數的結尾插入後置日誌 (Need fix...)
                        elif self.pointcut_define == "After":
                            for i in range(len(class_function.body)):
                                #print("Node body info: ", node.body[i])
                                if type(class_function.body[i]) == ast.If:
                                    #print("Find If.....")
                                    #print(node.body[i].body)
                                    if type(class_function.body[i].body[0]) == ast.Return:
                                    #    print("Setting After AOP.....")
                                        class_function.body[i].body.insert(-1, after_log[0])
                                elif type(class_function.body[i]) == ast.Return:
                                    class_function.body.insert(i, after_log[0])

                print("=================================================== Function Name ===================================================")
                print("Node name: " + class_function.name)
                print("=================================================== Node AST Information ===================================================")
                print("Node Information: " + ast.dump(class_function, indent=4))

        return node

class AST_Process:
    source_tree = ""
    before_advice_tree = ""
    after_advice_tree = ""
    target_function = ""

    pointcut_visit = Pointcut_Visitor()
    visit_before = Aspect_Visitor()
    visit_after = Aspect_Visitor()
    transformer = AOPTransformer()

    combined_tree = ""

    def Execution(self):
        # 為每個節點設置必要的行號（如果需要的話）
        ast.fix_missing_locations(self.combined_tree)
        print("=================================================== Combine Code In AST ===================================================")
        print(ast.dump(self.combined_tree, indent=4))
        print("=================================================== AST Convert To Code ===================================================")
        #print(ast.unparse(combined_tree))
        # 編譯並執行修改後的代碼

        print(ast.unparse(self.combined_tree))

        print("=================================================== Compile ===================================================")
        compile_code = compile(self.combined_tree, filename="<ast>", mode="exec")
        #print(compile_code)
        return compile_code


    def Pointcut_Process(self, Filepath, Function):
        code = open(Filepath, "r").read()
        self.source_tree = ast.parse(code)
        self.target_function = Function

        self.pointcut_visit.set_target_function(Function)
        print("=================================================== Source Code AST ===================================================")
        print(ast.dump(self.source_tree, indent=4))

        self.pointcut_visit.generic_visit(self.source_tree)

    def Before_Advice_Process(self, Advice_code):
        self.before_advice_tree = ast.parse(Advice_code)
        print("=================================================== Advice Code AST ===================================================")
        print(ast.dump(self.before_advice_tree, indent=4))

        self.visit_before.set_target("Before")
        self.visit_before.generic_visit(self.before_advice_tree)


        self.transformer.set_target(self.target_function, function_setting_array, "Before")
        transformed_tree = self.transformer.visit(self.source_tree)

        self.combined_tree = ast.Module(body=self.before_advice_tree.body + transformed_tree.body, type_ignores=[])

    def After_Advice_Process(self, Advice_code):
        self.after_advice_tree = ast.parse(Advice_code)
        print("=================================================== Advice Code AST ===================================================")
        print(ast.dump(self.after_advice_tree, indent=4))

        self.visit_after.set_target("After")
        self.visit_after.generic_visit(self.after_advice_tree)

        self.transformer.set_target(self.target_function, function_setting_array, "After")
        transformed_tree = self.transformer.visit(self.source_tree)

        self.combined_tree = ast.Module(body=self.after_advice_tree.body + transformed_tree.body, type_ignores=[])

ast_tree = AST_Process()

# Indenting advice code
def Code_Process(code):
    advice_code = inspect.getsource(code)
    lines = advice_code.split('\n')
    advice_code = '\n'.join(lines[1:])
    return autopep8.fix_code(advice_code)


def Aspect(cls):
    print(f"Catch class: {cls.__name__}...")
    compile_code = Weaver(cls())
    #print("Code: ", compile_code)
    exec(compile_code, globals())

    return cls

def Pointcut(Joinpoint, Pattern, Filepath, Function):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Function name: {func.__name__}")
            print(f"Joinpoint type: {Joinpoint}")
            print(f"Pattern: {Pattern}")
            print(f"Filepath: {Filepath}")
            print(f"Function: {Function}")

            ast_tree.Pointcut_Process(Filepath, Function)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def Before(param_func):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 呼叫傳入的函數參數
            result = param_func(*args, **kwargs)
            print(f"Function {func.__name__} is being called.")

            advice_code = Code_Process(func)

            print("========================================== Advice code ==========================================")
            print(advice_code)
            ast_tree.Before_Advice_Process(advice_code)

            #result = func()

            # 呼叫原始被裝飾的函數
            # return func
            return ast_tree.Execution()
        return wrapper
    return decorator

def After(param_func):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 呼叫傳入的函數參數
            result = param_func(*args, **kwargs)
            print(f"Function {func.__name__} is being called.")

            advice_code = Code_Process(func)

            print("========================================== Advice code ==========================================")
            print(advice_code)
            ast_tree.After_Advice_Process(advice_code)

            #result = func()

            # 呼叫原始被裝飾的函數
            # return func
            return ast_tree.Execution()
        return wrapper
    return decorator

def Weaver(Aspect):
    attributes = dir(Aspect)
    functions = [attr for attr in attributes if callable(getattr(Aspect, attr)) and not attr.startswith("__")]
    for func_name in functions:
        print(f"Function Name: {func_name}")
        func = getattr(Aspect, func_name)
        code = func()

    return code

# Problem:
# 1. Weaver(): Need to modify (func need target to execution)
# 2. Before、After、Around... multiple advice method need to implement

