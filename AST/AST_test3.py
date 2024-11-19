import ast
import inspect
import sys
import importlib.util
from pathlib import Path

class Pointcut_Visitor(ast.NodeVisitor):
    def Pointcut(self, pointcut_name):
        function_name = inspect.getsource(pointcut_name)
        print(function_name)
def print_source_from_other_directory(module_path):
    # 確定完整路徑
    module_path = Path(module_path)

    # 取得模組名稱（不包含副檔名）
    module_name = module_path.stem

    # 把模組所在的資料夾添加到 sys.path
    sys.path.append(str(module_path.parent))

    # 使用 importlib 導入該模組
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 使用 inspect.getsource() 打印整個模組的源代碼
    source_code = inspect.getsource(module)
    print(source_code)

    # 清理 sys.path
    sys.path.pop()

# 使用範例：假設 "other_folder/other_module.py" 是目標文件
print_source_from_other_directory("AST_test6.py")

def log():
    print("This is AOP Log insert...")

Pointcut_Visitor.Pointcut(log)