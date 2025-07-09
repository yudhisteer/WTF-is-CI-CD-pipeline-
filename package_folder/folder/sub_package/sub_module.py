from package_folder.folder.module1 import print_module

def print_sub_module(something: str):
    print(something)
    
if __name__ == "__main__":
    print_module("Hello from module1.py") 
    # This will not work because module1.py is in a higher level directory than sub_module.py unless we add the parent directory to the PYTHONPATH environment variable or use sys.path.insert(0, "/home/yoyo/CI-CD-Pipeline") or use a distribution package.