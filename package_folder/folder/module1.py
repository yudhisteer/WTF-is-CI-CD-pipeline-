def print_module(something: str) -> str:
    print(something)

CONSTANT = "MODULE7"
    

if __name__ == "__main__":
    from sub_package.sub_module import print_sub_module
    print_sub_module("Hello from sub_module.py")