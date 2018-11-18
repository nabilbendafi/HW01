#!/bin/bash

rm -rf dist && ./setup.py package && twine check dist/*whl

# Upload to TestPyPI
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Upload to PyPI
#twine upload dist/*
