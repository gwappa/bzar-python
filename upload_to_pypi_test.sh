#!/bin/bash

rm -rf dist
python3 setup.py sdist
python3 setup.py bdist_wheel
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
