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
Python packaging is a fundamental concept that enables developers to organize, distribute, and reuse code effectively. It provides a structured way to share `functionality` across projects and teams, ensuring that code is `maintainable`, `reproducible`, and `accessible`. Understanding how to package Python code is essential for any developer looking to contribute to the Python ecosystem or build robust applications.

1. Distributable
In basic terms, a package is a `distributable` set of Python code along with its metadata that can be reused by other developers.

2. Importable
It allows other developers to import the package and use its functions, classes, and variables in their own projects.

3. Reproducibility
We can use the same package in different system/machines and get the same results.


### 1.1 WTF is package/module/sub-package/distribution package?
Before diving into the technical details, let's clarify some fundamental concepts in Python packaging. Understanding the difference between `modules`, `packages`, `sub-packages`, and `distribution packages` is crucial for organizing and distributing your Python code effectively. These concepts form the foundation of Python's modular architecture and are essential for building maintainable and reusable software.


### 1.1.1 Module

A module in Python is a `self-contained unit of code` that can be `imported` and used in other Python programs. It can exist as either a single `.py` file or a directory containing multiple `.py` files. Modules encapsulate related functionality through `classes, functions, and variables`, making code more organized and reusable. They serve as the fundamental building blocks for structuring Python applications and sharing code between projects.

For example, consider a module named data_processing.py that contains functions to clean and transform data, such as `remove_duplicates`, `handle_missing_values`, and `normalize_numerical_columns`. You can import and use these functions in other Python scripts to process your datasets.

```python
# data_processing.py

def remove_duplicates(data):
    return list(set(data))

def handle_missing_values(data):
    return data.fillna(0)

def normalize_numerical_columns(data):
    return data.apply(lambda x: (x - x.mean()) / x.std())

def process_data(data):
    data = remove_duplicates(data)
    data = handle_missing_values(data)
    data = normalize_numerical_columns(data)
    return data
```

### 1.1.2 Package

A Python package is a directory containing `multiple Python modules organized together`. It is identified by the presence of an `__init__.py` file (which can be empty) that marks the directory as a package. This structure allows related modules to be grouped logically and imported as a single unit. 

For example, consider a package named `data_processing` that contains multiple modules for data cleaning, machine learning, and visualization. You can import and use these modules in other Python scripts to process your datasets. `data_cleaning.py`, `machine_learning.py`, and `visualization.py` are modules in this example.

```python
# data_processing

data_processing/
├── __init__.py
├── data_cleaning.py
├── machine_learning.py
└── visualization.py
```

We can import functions from the modules in the package `data_processing` in other Python scripts by using the following syntax:

```python
from data_processing.data_cleaning import remove_duplicates
from data_processing.machine_learning import train_model
from data_processing.visualization import plot_data
```

### 1.1.3 Sub-Package

A sub-package is a package that is nested within another package. It follows the same structure as a regular package, containing an `__init__.py` file and potentially other modules or sub-packages. Sub-packages help organize code hierarchically, allowing for more complex and structured applications.

For example, consider a comprehensive `machine_learning` package that contains sub-packages for different categories of algorithms:

```python
# machine_learning package structure

machine_learning/
├── __init__.py
├── utils.py
├── supervised/
│   ├── __init__.py
│   ├── linear_models.py
│   ├── tree_models.py
│   └── ensemble/
│       ├── __init__.py
│       ├── random_forest.py
│       └── gradient_boosting.py
├── unsupervised/
│   ├── __init__.py
│   ├── clustering.py
│   └── dimensionality_reduction.py
└── preprocessing/
    ├── __init__.py
    ├── scalers.py
    └── encoders.py
```

In this structure:
- `supervised/`, `unsupervised/`, and `preprocessing/` are **sub-packages** of the main `machine_learning` package
- `ensemble/` is a **sub-package** of the `supervised` sub-package (nested sub-package)
- Each sub-package has its own `__init__.py` file and can contain modules or additional sub-packages

You can import from these sub-packages like this:

```python
from machine_learning.supervised.linear_models import LinearRegression
from machine_learning.supervised.ensemble.random_forest import RandomForestClassifier
from machine_learning.unsupervised.clustering import KMeans
from machine_learning.preprocessing.scalers import StandardScaler
```

### 1.1.4 Distribution Package

A distribution package is a `versioned archive file` that contains a `Python package` along with its `metadata`, `dependencies`, and `installation instructions`. It's what gets uploaded to `PyPI` and installed via `pip install`. Note that `pip` is the package manager for Python. Other popular package managers for Python are `conda` and `poetry` and the one I like `uv`.

Distribution packages come in different formats like `source distributions (sdist)` and `wheels` which we will see in a moment. Some well-known examples of distribution packages are `numpy`, `fast-api`, and `pandas`, etc.


------------------------------------------------------------------------------------------------

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