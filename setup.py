#!/usr/bin/env python

import codecs
import os
import sys

from setuptools import setup, find_packages

os.chdir(os.path.dirname(sys.argv[0]) or ".")

with codecs.open('README.rst', 'r', 'utf-8') as f:
    long_description = f.read()

setup(
    name="libzbar-cffi",
    version="0.2.0",
    description="Efficient cffi-based bindings for the zbar QR decoder (Py2, Py3, and PyPy)",
    long_description=long_description,
    url="https://github.com/wolever/libzbar-cffi",
    author="David Wolever",
    author_email="david@wolever.net",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: BSD License",
    ],
    packages=find_packages(),
    install_requires=["cffi>=1.0.0"],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["./libzbar/ffi_build.py:ffi"],
)
