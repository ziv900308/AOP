import ast
from test_code import *

function_setting_array = []

def function(x):
    return x + 117

def set_node_lineno(node, lineno, col_offset=0):
    node.lineno = lineno
    node.col_offset = col_offset
    return node

class Visitor(ast.NodeVisitor):
    def visit_Attribute(self, node):
        print("=================================================== Attribute Name ===================================================")
        print('Attribute: ' + node.attr)
        name = ast.dump(node.value)
        if 'calculatorService' in name and node.attr not in function_setting_array:
            print("Find!!")
            print("node information: " + name)
            function_setting_array.append(node.attr)
        print(ast.dump(node))
        ast.NodeVisitor.generic_visit(self, node)

    # def generic_visit(self, node):
    #     print(node.__class__.__name__)
    #     ast.NodeVisitor.generic_visit(self, node)

# 定義切面：在每個函數執行前後加入日誌記錄
class AOPTransformer(ast.NodeTransformer):
    target_class = ""
    target_function = ""

    def set_target(self, target_class, target_function):
        print("Setting target...")
        self.target_class = target_class
        self.target_function = target_function

    def visit_If(self, node):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++ Node If information: ", node.body)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        print("Target class: " + self.target_class)
        #print("Target function: " + self.target_function)
        # # 日誌前置通知
        before_log = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='log', ctx=ast.Load()),
                args=[ast.Constant(value=f"Entering {node.name}")],
                keywords=[]
            )
        )
        before_log = set_node_lineno(before_log, node.lineno)

        # # 日誌後置通知
        after_log = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='log', ctx=ast.Load()),
                args=[ast.Constant(value=f"Exiting {node.name}")],
                keywords=[]
            )
        )
        after_log = set_node_lineno(after_log, node.lineno + len(node.body) + 1)

        for target in self.target_function:
            if node.name == target:
                # # 在函數的開頭插入前置日誌
                node.body.insert(0, before_log)
                # # 在函數的結尾插入後置日誌
                for i in range(len(node.body)):
                    #print("Node body info: ", node.body[i])
                    if type(node.body[i]) == ast.If:
                        #print("Find If.....")
                        #print(node.body[i].body)
                        if type(node.body[i].body[0]) == ast.Return:
                        #    print("Setting After AOP.....")
                            node.body[i].body.insert(-1, after_log)
                    elif type(node.body[i]) == ast.Return:
                        node.body.insert(i, after_log)

        print("=================================================== Function Name ===================================================")
        print("Node name: " + node.name)
        print("=================================================== Node AST Information ===================================================")
        print("Node Information: " + ast.dump(node, indent=4))

        return node

    # def visit_Attribute(self, node):
    #     print("=================================================== Function Name ===================================================")
    #     print('Attribute node: ' + node.attr)
    #     name = ast.dump(node.value)
    #     if 'calculatorService' in name:
    #         print("Find!!")
    #         print("=================================================== Node AST Information ===================================================")
    #         print("Node information: " + name)
    #     print(ast.dump(node))
    #     ast.NodeVisitor.generic_visit(self, node)

code = open("D:/Python/AST/test_code.py", "r").read()

# 日誌功能的代碼片段
log_code = """
def log(message):
    print(f"LOG: {message}")
"""

tree = ast.parse(code)

log_tree = ast.parse(log_code)

print("=================================================== Source Code AST ===================================================")
print(ast.dump(tree, indent=4))

print("=================================================== LOG Code AST ===================================================")
print(ast.dump(log_tree, indent=4))

tree_visitor = Visitor()
tree_visitor.generic_visit(tree)

print("=================================================== Function setting Array ===================================================")

transformer = AOPTransformer()
transformer.set_target("calculatorService", function_setting_array)
transformed_tree = transformer.visit(tree)

print("=================================================== Function setting Array ===================================================")
for func in function_setting_array:
    print("Function: ", func)

# 將日誌功能的AST與主代碼的AST合併
combined_tree = ast.Module(body=log_tree.body + transformed_tree.body, type_ignores=[])

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
需要注意不能只改單一問題
需定義好範圍 (哪個範圍的pointcut)
只轉Advice成AST就夠了 還是其他方法?
PPT想法整理

參考AspectJ早期的作法
Flow Diagram: 不要寫得太細項 寫目標

Join Point、Pointcut implementation mechanism...

計劃書 (aspectlib、)

"""
