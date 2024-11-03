from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:

    requirement_list:List[str] = []
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()
            
            for line in lines:
                requirement = line.strip()
                
                if requirement and requirement!='-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("REQUIREMENT FILE NOT FOUND")
        
    return requirement_list

setup(
    name="Network Security",
    version="0.0.1",
    author="Kevin Joy",
    author_email="kevinjoythomas2004@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)