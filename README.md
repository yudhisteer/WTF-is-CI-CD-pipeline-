# What the F@*#K is a CI/CD Pipeline?

Thanks to Eric Riddoch for the inspiration to write this project. Note: ChatGPT helped me write this README. Just kidding! I used Claude and Grok.

[under-construction]

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
Have you every written a piece of code on your computer only to find out later that you cannot run it on your friend's computer or you cannot run it on your own computer after a few months because some dependencies changed? Well, that's why we package!
Python packaging enables developers to `organize`, `distribute`, and `reuse code` effectively. Pause here and ponder about these 3 words I highlighted.
It provides a structured way to share `functionality` across projects and teams, ensuring that code is `maintainable`, `reproducible`, and `accessible`.

**Distributable:**

In basic terms, a package is a `distributable` set of Python code along with its metadata that can be reused by other developers. Voila!

**Importable:**

It allows other developers to import the package and use its functions, classes, and variables in their own projects.

**Reproducibility:**
   
We can use the same package in different system/machines and get the same results.


### 1.1 WTF is package/module/sub-package/distribution package?
Before diving into the technical details, let's clarify some fundamental concepts in Python packaging. Understanding the difference between `modules`, `packages`, `sub-packages`, and `distribution packages` is crucial for organizing and distributing our Python code effectively. These concepts form the foundation of Python's `modular architecture` and are essential for building `maintainable` and `reusable` software.


### 1.1.1 Module

A module in Python is a `self-contained unit of code` that can be `imported` and used in other Python programs. It can exist as either a single `.py` file or a directory containing multiple `.py` files. 
Modules encapsulate related functionality through `classes, functions, and variables`, making code more organized and reusable. They serve as the fundamental building blocks for structuring Python applications and sharing code between projects.

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

A sub-package is a package that is nested within another package - who thought? It follows the same structure as a regular package, containing an `__init__.py` file and potentially other modules or sub-packages. 
Sub-packages help organize code hierarchically, allowing for more complex and structured applications.

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
Sometimes we need to import modules in a way that's not strictly following Python's import system. While this isn't recommended for production code, it can be useful for quick scripts, testing, or when dealing with legacy code. Here are some common "hacky" ways to import modules:

1. Using `sys.path` manipulation
2. Using `PYTHONPATH` environment variable
3. Using relative imports with `..` notation
4. Using `importlib` for dynamic imports

Let's explore these methods and understand when they might be useful (and when they should be avoided).


### 2.1 PATH

This command below will print the directories in your PATH. The directories in `PATH` are separated by colons `(:)` on Linux/macOS or semicolons `(;)` on Windows. When you run a command, the shell searches these directories in order from left to right until it finds an executable with that name. 

```bash
echo $PATH
```


Let's say our `PATH` looks like this:

```bash
PATH=/usr/local/bin:/usr/bin:/bin:/home/user/.local/bin
```

Run `echo $PATH` to see the directories in your PATH.

First, check /usr/local/bin/ - Is there a file called python here?
- If YES: Run /usr/local/bin/python and STOP searching
- If NO: Continue to next directory

Next, check /usr/bin/ - Is there a file called python here?
- If YES: Run /usr/bin/python and STOP searching
- If NO: Continue to next directory

And so on...

Note:
If we have multiple versions of the same program, the first one found wins.





### 2.1 PYTHONPATH

`PYTHONPATH` is an environment variable in Python that specifies additional directories for the interpreter to search for modules and packages. This helps Python find code that isn't in the standard library or current directory.  It's like `PATH` for executables, but specifically for Python modules.


When Python encounters an import statement, it searches through directories in this specific order:
- Current directory (where your script is running)
- PYTHONPATH directories (what you add)
- Standard library directories (built-in Python modules)
- Site-packages directories (installed packages like `pip install numpy`)


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

The answer is no. This is because `sub_package/sub_module.py` is in a lower level directory than `module1.py` and `module2.py`. (trying to import "upward")

We get the following error:

```python
# In sub_package/sub_module.py
from ..module1 import print_module  # This fails!
# Error: ImportError: attempted relative import with no known parent package
```

We need to add the parent directory to `PYTHONPATH` so Python can find the modules:

```bash
# Add the parent directory to PYTHONPATH
PYTHONPATH=$PYTHONPATH:/home/yoyo/CI-CD-Pipeline/package_folder/folder

# Now run your script
python package_folder/folder/sub_package/sub_module.py
```

Now in `sub_module.py`, we can import directly:

```py
from module1 import print_module  # This works!
```


or we add the `project root` to `PYTHONPATH` and import the module directly:

```bash
# Add the project root
PYTHONPATH=$PYTHONPATH:/home/yoyo/CI-CD-Pipeline/

# Run the script
python package_folder/folder/sub_package/sub_module.py
```

Now we can use full paths:

```python
from package_folder.folder.module1 import print_module  # This works!
```


In summary:

When we run:

```python
from module1 import print_module
```

Python searches in this order:
- Current directory: `/home/yoyo/CI-CD-Pipeline/package_folder/folder/sub_package/` ❌
- PYTHONPATH: `/home/yoyo/CI-CD-Pipeline/package_folder/folder/` ✅ Found it!
- Standard library: `/usr/lib/python3.x/` (not checked, already found)
- Site-packages: (not checked, already found)

Key Takeaway: `PYTHONPATH` helps Python find modules that aren't in the standard locations, especially when dealing with complex project structures where you need to import from different directory levels.


### 2.2 Python's Search Path

Instead of setting `PYTHONPATH`, you can modify Python's search path directly.

```python
import sys
sys.path.insert(0, "/home/yoyo/CI-CD-Pipeline")
from package_folder.folder.module1 import print_module
```

This adds `/home/yoyo/CI-CD-Pipeline` to the start of Python's module search path (`sys.path`), allowing us to import `print_module` from `package_folder.folder.module1` even though `sub_module.py` is in a subdirectory. This bypasses normal import restrictions due to directory structure.

```
BEFORE inserting:
0: /current/working/directory
1: /usr/lib/python311.zip
2: /usr/lib/python3.11
3: /usr/lib/python3.11/lib-dynload
4: /home/user/.local/lib/python3.11/site-packages

==================================================

AFTER inserting:
0: /home/yoyo/CI-CD-Pipeline              ← NEW! Added at position 0
1: /current/working/directory             ← Everything else shifted down
2: /usr/lib/python311.zip
3: /usr/lib/python3.11
4: /usr/lib/python3.11/lib-dynload
5: /home/user/.local/lib/python3.11/site-packages
```


#### Python's Search Path vs PYTHONPATH

#### sys.path
- **What it is**: A list inside Python containing all directories Python will search
- **When created**: Every time Python starts
- **How to view**: `import sys; print(sys.path)`

#### PYTHONPATH
- **What it is**: An environment variable (like PATH) set in your shell
- **When used**: Only when Python starts - gets added to sys.path
- **How to view**: `echo $PYTHONPATH` (in terminal)

```python
# Terminal: PYTHONPATH=/home/yoyo/project1:/home/yoyo/project2

# When Python starts, sys.path becomes:
import sys
print(sys.path)

# Output:
[
    '/current/directory',           # Always first
    '/home/yoyo/project1',         # From PYTHONPATH
    '/home/yoyo/project2',         # From PYTHONPATH  
    '/usr/lib/python3.11',         # Standard library
    '/usr/lib/python3.11/site-packages'  # Installed packages
]
```


#### Key Differences

| Aspect | PYTHONPATH | sys.path |
|--------|------------|----------|
| Type | Environment variable | Python list |
| When set | Before running Python | During Python execution |
| Scope | Affects all Python processes | Only current Python process |
| Persistence | Survives across Python sessions | Lost when Python exits |
| How to modify | `export PYTHONPATH=...` | `sys.path.insert()` or `sys.path.append()` |

```bash
# Method 1: Using PYTHONPATH (affects ALL Python sessions)
export PYTHONPATH=/home/yoyo/myproject:$PYTHONPATH
python my_script.py

# Method 2: Using sys.path.insert() (affects ONLY current script)
python -c "
import sys
sys.path.insert(0, '/home/yoyo/myproject')
print('Path added successfully')
print(sys.path[:3])
"
```

### 2.3 Why These Approaches are "Hacky" and Should Be Avoided

While `PYTHONPATH` and `sys.path` manipulation can solve immediate import problems, they create significant issues in professional development:

#### Problems with Our Examples:

#### 1. **Environment Dependency**
```bash
# This only works on MY machine:
PYTHONPATH=$PYTHONPATH:/home/yoyo/CI-CD-Pipeline/package_folder/folder
python package_folder/folder/sub_package/sub_module.py
```
**Problem**: The path `/home/yoyo/CI-CD-Pipeline` is hardcoded to our specific machine. When a colleague tries to run this code, it will fail because they don't have the same directory structure.

#### 2. **Hardcoded Paths**
```python
import sys
sys.path.insert(0, "/home/yoyo/CI-CD-Pipeline")  # Hardcoded!
from package_folder.folder.module1 import print_module
```
**Problem**: This path is specific to our system. The code becomes non-portable and breaks in different environments (development, testing, production).

#### 3. **No Dependency Management**
```python
# Our current approach:
from module1 import print_module  # What if module1 needs other libraries?
```
**Problem**: There's no way to specify what dependencies `module1` needs. If it requires `numpy` or `pandas`, users have to figure that out themselves.

What NOT to do:

**Hacky Way (Current):**
```bash
# Instructions to run your code:
# 1. Clone the repository
# 2. Set PYTHONPATH=/home/yoyo/CI-CD-Pipeline
# 3. Make sure you're in the right directory
# 4. Cross your fingers and run: python package_folder/folder/sub_package/sub_module.py
```

What to do:

**Professional Way (Distribution Package):**
```bash
# Instructions to run your code:
pip install my-package
python -c "from my_package.sub_package import sub_module; sub_module.run()"
```

#### The Better Way: Distribution Packages

Instead of manipulating paths, the professional approach is to create a proper package structure which we will see in the next section:

```bash
# Instead of our current structure:
my_package/
├── __init__.py
├── module1.py
├── module2.py
└── sub_package/
    ├── __init__.py
    └── sub_module.py

# Create a proper distribution package:
my_package/
├── pyproject.toml           # Package metadata & dependencies
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── module1.py
│       ├── module2.py
│       └── sub_package/
│           ├── __init__.py
│           └── sub_module.py
└── README.md
```

In the next section, we'll learn how to build proper distribution packages that solve all these problems elegantly!

---------------------------------------

## 3. Building a Distribution Package
[python.org](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package) describes a distribution package as *"A versioned archive file that contains Python packages, modules, and other resource files that are used to distribute a Release. The archive file is what an end-user will download from the internet and install."* I cannot explain it better.


### 3.1 Packaging with setup.py

Back in the 1990s, Python’s standard library included a module called `Distutils`, which provided tools for creating distribution packages. However, Distutils had many shortcomings—most notably, it was difficult and unintuitive to use.

To address these issues, a third-party project called `setuptools` was created. Setuptools acted as a more user-friendly wrapper around Distutils, and over time, it became the de facto standard for building and distributing Python packages. Even today, setuptools remains the most widely supported tool for this purpose, though there are now several modern alternatives (which we’ll discuss later).

In this section, we’ll look at the traditional approach to packaging: using setuptools with a `setup.py` file to create a distribution package.

```python
# setup.py

from setuptools import setup

setup(
    name="packaging", # name of the package
    version="0.0.0", # semantic versioning
    author="Yoyo", # name of the author
    packages=["package_folder"], # packages to include in the distribution
    author_email="yoyo@example.com", # email of the author
    description="A sample Python package", # description of the package
    long_description=open("README.md").read(), # long description of the package
    license="MIT", # license of the package
)
```

The `setup.py` is a CLI tool such that the `setup()` function picks up CLI arguments that we pass into the Python commands. Therefore, we can use:

```bash
python setup.py --help
```

To build the package, we can use:

```bash
python setup.py build sdist
```

Bu running this command we create a `dist` folder with the following structure:

```bash
dist/
└── packaging-0.0.0.tar.gz
```

The `tar.gz` file is the `source distribution`(sdist), that is an installable version of our code which means we can install it using pip as such:

```bash
pip install ./dist/packaging-0.0.0.tar.gz
```

We can verify by using:

```bash
pip list
```

Note we will also have a copy of our code in the `site-packages` folder inside our virtual environment. Therefore, we can import the `print_module` function from `package_folder.folder.module1` directly as such without having to use the `sys.path` manipulation or `PYTHONPATH` environment variable.

```python
# In sub_package/sub_module.py

from package_folder.folder.module1 import print_module

print_module("Hello from module1.py") # This works!
```

We can use the `find_packages()` function to find all packages in the current directory. However, it is important that we have a `__init__.py` file in the package directory or in the sub-package directory or else the `find_packages()` function will not find the necessary package.

```python
# setup.py

from setuptools import setup, find_packages

setup(
    ...
    packages=find_packages(), # find all packages in the current directory
    ...
)
```

It may seem like a lot of effort just to get a simple import statement working, but there's a big benefit: once you've built your distribution package, you can upload it to `PyPI` (I'll show you how later). Then, when someone runs `pip install <your-package-name>`, they're actually downloading that `tar.gz` file and installing it into their own virtual environment—ready to import and use, no manual path hacks required!

Suppose we make some changes in the `package_folder/folder/module1.py` file and run the python file. Will we see the changes? The answer is no because we are still using the built and installed distribution package in the `site-packages` folder in our virtual environment. But we cannot build and install the package everytime we make some changed. Instead we can do:

Use `pip install -e .` during development when you're actively working on the code where `e` stands for `editable`.

Use `pip install .` when you want to install a stable version or for production.



### 3.2 sdist and wheel formats

### 3.3 From setup.py to setup.cfg

### 3.4 From setup.cfg to pyproject.toml

### 3.5 Packaging datafiles with/out MANIFEST.in


---------------------------------------

## 4. CI

## 5. CD
