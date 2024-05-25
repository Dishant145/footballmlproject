
from setuptools import find_packages
from typing import List
from distutils.core import setup

def get_requirements(file_path):
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirements]

    return requirements

setup(name='FootballProject',
      version='1.0',
      author='Dishant',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=find_packages(),
      install_requires = get_requirements('requirements.txt')
     )