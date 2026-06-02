from setuptools import find_packages, setup
from typing import List


def get_requirements() -> List[str]:
    """

    """
    requirement_list : list[str] = []
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                requirement = line.strip()
                if requirement and not requirement.startswith(('#', '-e')):
                    requirement_list.append(requirement)
            
    except FileNotFoundError:
        print("requirements.txt file not found")
    
    return requirement_list


setup(
    name= "NetworkSecurity",
    version= "0.0.1",
    author= "Mohammad Reza Rajaee",
    author_email= "m.r.r.sayron@gmail.com",
    packages= find_packages(),
    install_requires= get_requirements()
)

