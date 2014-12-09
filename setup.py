#!/usr/bin/env python
# -*- coding: utf-8 -*-
from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

requires = [
    'schema>=0.3.1',
    'requests>=2.5.0',
]

setup(
    name='durga',
    version='0.1.0',
    description='Create easy to use Python objects for REST resources including schema validation.',  # noqa
    long_description=readme,
    author='transcode',
    author_email='team@transcode.de',
    url='https://github.com/transcode-de/durga',
    packages=[
        'durga',
    ],
    package_dir={'durga': 'durga'},
    include_package_data=True,
    install_requires=requires,
    license='BSD',
    zip_safe=False,
    keywords='durga',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
