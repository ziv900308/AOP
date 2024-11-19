import ast
import inspect
from test_code import *

before_log = []
after_log = []
function_setting_array = []

def set_node_lineno(node, lineno, col_offset=0):
    node.lineno = lineno
    node.col_offset = col_offset
    return node

class Pointcut_Visitor(ast.NodeVisitor):
    def visit_ClassDef(self, node):
        if 'CalculatorService' == node.name:
            print("=================================================== Class Information ===================================================")
            #print("Node class information:", ast.dump(node, indent=4))
            print("Node class name:", node.name)

            for class_body in node.body:
                # print("Node class function:", ast.dump(class_body, indent=4))
                print("Node class function name:", class_body.name)
                if class_body.name not in function_setting_array:
                    function_setting_array.append(class_body.name)

        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        if 'Test' == node.name:
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

    def visit_FunctionDef(self, node):
        for target in self.target_function:
            if node.name == target:
                # # 在函數的開頭插入前置日誌
                node.body.insert(0, before_log[0])
                # # 在函數的結尾插入後置日誌 (Need fix...)
                for i in range(len(node.body)):
                    #print("Node body info: ", node.body[i])
                    if type(node.body[i]) == ast.If:
                        #print("Find If.....")
                        #print(node.body[i].body)
                        if type(node.body[i].body[0]) == ast.Return:
                        #    print("Setting After AOP.....")
                            node.body[i].body.insert(-1, after_log[0])
                    elif type(node.body[i]) == ast.Return:
                        node.body.insert(i, after_log[0])
                    elif type(node.body[i]) != ast.Return and i == len(node.body) - 1:
                        node.body.insert(i + 1, after_log[0])


        print("=================================================== Function Name ===================================================")
        print("Node name: " + node.name)
        print("=================================================== Node AST Information ===================================================")
        print("Node Information: " + ast.dump(node, indent=4))

        return node

code = open("C:/Users/Boss Hsu/Python_Code/AST/test_code.py", "r").read()

log_code_before = """
def log_Before(*args, **kwargs):
    print("This is AOP Log insert before...")
"""

log_code_after = """
def log_After():
    print("This is AOP Log insert after...")
"""

tree = ast.parse(code)
log_tree_before = ast.parse(log_code_before)
log_tree_after = ast.parse(log_code_after)


print("=================================================== Source Code AST ===================================================")
print(ast.dump(log_tree_before, indent=4))

pointcut_visit = Pointcut_Visitor()
pointcut_visit.generic_visit(tree)

visit_before = Aspect_Visitor()
visit_before.set_target("Before")
visit_before.generic_visit(log_tree_before)

visit_after = Aspect_Visitor()
visit_after.set_target("After")
visit_after.generic_visit(log_tree_after)

transformer = AOPTransformer()

transformer.set_target("CalculatorService", function_setting_array, "Before")
transformed_tree = transformer.visit(tree)

transformer.set_target("CalculatorService", function_setting_array, "After")
transformed_tree = transformer.visit(tree)

print("=================================================== Function setting Array ===================================================")
for func in function_setting_array:
    print("Function: ", func)

# 將日誌功能的AST與主代碼的AST合併
combined_tree = ast.Module(body=log_tree_before.body + log_tree_after.body + transformed_tree.body, type_ignores=[])


# 為每個節點設置必要的行號（如果需要的話）
ast.fix_missing_locations(combined_tree)
print("=================================================== Combine Code In AST ===================================================")
print(ast.dump(combined_tree, indent=4))
print("=================================================== After AOP Compile ===================================================")
#print(ast.unparse(combined_tree))
# 編譯並執行修改後的代碼

print(ast.unparse(combined_tree))

print("=================================================== Origin Result ===================================================")
main()
exec(compile(combined_tree, filename="<ast>", mode="exec"))

print("=================================================== Execution Result ===================================================")
main()

"""
待做事項:
loose typing 特性 這部份自己怎麼處理

"""