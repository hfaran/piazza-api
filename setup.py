from __future__ import print_function

import codecs
import os
from setuptools import setup, find_packages

import piazza_api


def read(filename):
    """Read and return `filename` in root dir of project and return string"""
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, filename), 'r').read()


install_requires = read("requirements.txt").split()
long_description = read('README.md')


setup(
    name='piazza-api',
    version=piazza_api.__version__,
    url='http://github.com/hfaran/piazza-api/',
    license='MIT License',
    author='Hamza Faran',
    install_requires=install_requires,
    description="Unofficial Client for Piazza's Internal API",
    long_description=long_description,
    packages=['piazza_api'],
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
