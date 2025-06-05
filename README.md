# CI-CD-Pipeline


## Table of Contents
1. Why Package?
    - WTF is package/module/sub-package/distribution package?
2. Importing Modules in a Hacky Way
    - PYTHONPATH
    - sys.path.insert(0, path)
3. Building a Distribution Package
    - sdist and wheel formats
    - Packaging with setup.py
    - From setup.py to setup.cfg
    - From setup.cfg to pyproject.toml
    - Packaging datafiles with/out MANIFEST.in
4. CI
5. CD


---------------------------------------

## 1. Why Package?

1. Distributable
In basic terms, a package is a `distributable` set of Python code along with its metadata that can be reused by other developers.

2. Importable
It allows other developers to import the package and use its functions, classes, and variables in their own projects.

3. Reproducibility
We can use the same package in different system/machines and get the same results.




### 1.1 WTF is package/module/sub-package/distribution package?

A module is a single piece of an import path in Python. It can be a single file or a directory. 

A package is a collection of modules.

A sub-package is a sub-directory of a package.

A distribution package is a package that is distributed to other developers.

## 2. Importing Modules in a Hacky Way

### 2.1 PYTHONPATH

`PYTHONPATH` is an environment variable in Python that specifies additional directories for the interpreter to search for modules and packages. This helps Python find code that isn't in the standard library or current directory.

Let's see when and why to use it. Suppose we have the dir structure below:

```
my_package/
├── __init__.py
├── module1.py
├── module2.py
└── sub_package/
    ├── __init__.py
    └── sub_module.py
```

In `module1.py` and/or `module2.py`, we are able to import functions/classes/variables from `sub_package/sub_module.py`. This is because `module1.py` and `module2.py` are in a higher level directory than `sub_package/sub_module.py`.

But can we import  functions/classes/variables from `module1.py` and/or `module2.py` in `sub_package/sub_module.py`?

The answer is no. This is because `sub_package/sub_module.py` is in a lower level directory than `module1.py` and `module2.py`.

We get the following error:

```python
from ..module1 import print_module
ImportError: attempted relative import with no known parent package
```

So we need to add the path of the parent directory of `package_folder` to the `PYTHONPATH` environment variable.

PYTHONPATH adds directories to Python's `sys.path`. When Python encounters an import, it searches through sys.path in order:
- Current directory
- PYTHONPATH directories  
- Standard library directories
- Site-packages directories

```bash
PYTHONPATH=$PYTHONPATH:/home/yoyo/CI-CD-Pipeline/package_folder/folder python package_folder/folder/sub_package/sub_module.py
```

```python
from module1 import print_module
    
if __name__ == "__main__":
    print_module("Hello from module1.py") 
```

or 

```bash
PYTHONPATH=$PYTHONPATH:/home/yoyo/CI-CD-Pipeline/ python package_folder/folder/sub_package/sub_module.py  
```

```python
from package_folder.folder.module1 import print_module

    
if __name__ == "__main__":
    print_module("Hello from module1.py") 
```

### 2.2 sys.path.insert(0, path)

Another way if we do not want to add the path to the `PYTHONPATH` environment variable is to use `sys.path.insert(0, path)` in the `sub_module.py`.

```python
import sys
sys.path.insert(0, "/home/yoyo/CI-CD-Pipeline")
from package_folder.folder.module1 import print_module
    
if __name__ == "__main__":
    print_module("Hello from module1.py") 
```

This adds `/home/yoyo/CI-CD-Pipeline` to the start of Python's module search path (`sys.path`), allowing us to import `print_module` from `package_folder.folder.module1` even though `sub_module.py` is in a subdirectory. This bypasses normal import restrictions due to directory structure.


---------------------------------------

## 3. Building a Distribution Package

### 3.1 sdist and wheel formats

### 3.2 Packaging with setup.py

### 3.3 From setup.py to setup.cfg

### 3.4 From setup.cfg to pyproject.toml

### 3.5 Packaging datafiles with/out MANIFEST.in


---------------------------------------

## 4. CI

## 5. CD