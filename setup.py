from setuptools import setup, find_packages

setup(
    name="yoyo-package", # name of the package
    version="0.0.0", # semantic versioning
    author="Yoyo", # name of the author
    packages=find_packages(), # find all packages in the current directory
    author_email="yoyo@example.com", # email of the author
    description="A sample Python package", # description of the package
    long_description=open("README.md").read(), # long description of the package
    license="MIT", # license of the package
)