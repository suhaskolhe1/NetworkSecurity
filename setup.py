from setuptools import find_packages,setup
from typing import List

def get_requirement()-> List[str]:
    """
    Docstring for get_requirement
    
    :return: list of requirements
    :rtype: List[str]
    """
    req_list:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines =file.readlines()
            for line in lines:
                req =line.strip()
                if req and req !='-e .':
                    req_list.append(req)
    except FileNotFoundError:
        print("Requiements.txt Not Found")
    return req_list

print(get_requirement())



setup(
    name='Network Security',
    version='0.1',
    author='Suhas Kolhe',
    author_email='suhaskolhe1111@gmail.com',
    packages=find_packages(),
    install_requires=get_requirement(),
)