#!/usr/bin/env python3
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='hw01',
    version='1.0.0',
    description='Python library to work with Lenovo HW01',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Nabil BENDAFI',
    author_email='nabil@bendafi.fr',
    url='https://github.com/nabilbendafi/hw01',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['bluepy'],
    tests_suite='nose.collector',
    tests_require=[
        'nose',
        'coverage',
    ]
)

