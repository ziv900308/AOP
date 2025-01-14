from setuptools import setup, find_packages

setup(
    name="Weaver",                 # 模組名稱
    version="1.0.0",               # 版本號
    description="A Python file compiler module",  # 簡短描述
    packages=find_packages(),      # 自動搜尋並包含所有模組
    install_requires=[],           # 依賴包清單（如果有其他依賴，列在這裡）
    entry_points={
        "console_scripts": [
            "Weaver=Weaver.Weaver:main",  # 添加命令行入口，執行 `Weaver`
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',       # Python 版本要求
)