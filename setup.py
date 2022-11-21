
"""
It is a python file, the presence of which is an indication that the module/package you are about 
to install has likely been packaged and distributed with Distutils, 
Which is the standard for distributing Python Modules.

"This file is to install current code as library

Description: This function is going to return list of requirement
mention in requirements.txt file
return This function is going to return a list which contain name
of libraries mentioned in requirements.txt file

# metadata about packages

"""

from setuptools import find_packages,setup
from typing import List

REQUIREMENT_FILE_NAME="requirements.txt"
HYPEN_E = "-e ."
NAME = "sensor"
VERSION = "0.0.1" 
AUTHOR = "Nikhil"
EMAIL = "nikhilchhabra877@gmail.com"

def get_requirements()->List[str]:
    """
    This function returns list of packages required for this project
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_file = requirement_file.readlines()
        requirement_file = [names.replace("\n","") for names in requirement_file]
        if HYPEN_E in requirement_file:
            requirement_file.remove(HYPEN_E)
        return requirement_file



setup(name = NAME,
    version = VERSION,
    author = AUTHOR,
    email = EMAIL,
    packages = find_packages(),
    install_requires = get_requirements())