from setuptools import setup, find_packages
import os

os.environ['SETUPTOOLS_ENABLE_FEATURES'] = 'legacy-editable'

setup(
    name='MyHelperLibrary',
    version='0.1',
    packages=find_packages(include=['MyHelperLibrary', 'MyHelperLibrary.Helpers']),
    description='A Python library of helpful methods',
    author='Kieran',
    python_requires='>=3.6',
    install_requires=[
        'pyside6>=6.0',
    ],
    extras_require={
        'dev': ['pytest', 'icecream'],
    },
)
