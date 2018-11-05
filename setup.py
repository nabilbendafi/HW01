#!/usr/bin/env python3
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='hw01',
    version='0.0.1',
    description='Python library to work with Lenovo HW01',
    long_description=readme,
    author='Nabil BENDAFI',
    author_email='nabil@bendafi.fr',
    url='https://github.com/nabilbendafi/hw01',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['bluepy'],
    tests_suite='nose.collector',
    tests_require=[
        'nose',
        'coverage',
    ]
)

