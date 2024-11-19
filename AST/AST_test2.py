import ast

# AOP test code
log_code = """
def log(message):
    print(f"LOG: {message}")
"""


def set_node_lineno(node, lineno, col_offset=0):
    node.lineno = lineno
    node.col_offset = col_offset
    return node


# 定義切面：在每個函數執行前後加入日誌記錄
class AOPTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # 日誌前置通知 (before)
        before_log = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='log', ctx=ast.Load()),
                args=[ast.Constant(value=f"Entering {node.name}")],
                keywords=[]
            )
        )
        before_log = set_node_lineno(before_log, node.lineno)

        # 日誌後置通知
        after_log = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='log', ctx=ast.Load()),
                args=[ast.Constant(value=f"Exiting {node.name}")],
                keywords=[]
            )
        )
        after_log = set_node_lineno(after_log, node.lineno + len(node.body) + 1)

        # 在函數的開頭插入前置日誌
        node.body.insert(0, before_log)
        # 在函數的結尾插入後置日誌
        node.body.append(after_log)

        return node

code = open('D:/Python/AOP/AOP_Project_Test/App_test.py', 'r').read()
node = ast.parse(code)
print(ast.dump(node, indent=4))


log_tree = ast.parse(log_code)

transformer = AOPTransformer()
transformed_tree = transformer.visit(node)

# 將日誌功能的AST與主代碼的AST合併
combined_tree = ast.Module(body=log_tree.body + transformed_tree.body, type_ignores=[])

# 為每個節點設置必要的行號（如果需要的話）
ast.fix_missing_locations(combined_tree)
print("===================================================")
print(ast.dump(combined_tree, indent=4))
print("88888888888888888888888888888888888888888888888888888")

print(ast.unparse(combined_tree))
#print(ast.unparse(combined_tree))
# 編譯並執行修改後的代碼
exec(compile(combined_tree, filename="<ast>", mode="exec"))

print(ast.unparse(combined_tree))