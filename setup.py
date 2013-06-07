#!/usr/bin/env python
import dopy

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='dopy',
    version=dopy.__version__,
    description="A Python client for the Digital Ocean API",
    url="https://github.com/devo-ps/dopy",
    packages=['dopy'],
    install_requires = ["requests >= 1.0.4"],
)
