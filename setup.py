# coding: utf-8

import re
from setuptools import setup


def fread(filepath):
    with open(filepath, 'rb') as f:
        return f.read().decode('utf-8')


m = re.findall(r'__version__\s*=\s*\'(.*)\'', fread('exchange.py'))
version = m[0]


setup(
    name='exchange',
    version=version,
    author='Hsiaoming Yang',
    author_email='me@lepture.com',
    url='https://github.com/akarat/exchange',
    py_modules=['exchange'],
    description='Get the current exchange rate.',
    long_description=fread('README.rst'),
    license='BSD',
    platforms='any',
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
