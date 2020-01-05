#!/usr/bin/env python

from distutils.core import setup

setup(
    name='familytree',
    version='0.1.0',
    description='Simple family tree diagram generator',
    author='Toshinori Hanya',
    url='https://github.com/t-hanya/family-tree',
    license='MIT',
    packages=['familytree', 'familytree.layout', 'familytree.html'],
    entry_points = {
        'console_scripts': ['familytree=familytree.html.generate:main'],
    },
)
