#!/usr/bin/env python
import dopy

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(filename):
    return open(filename).read()

setup(
    name="dopy",
    version=dopy.__version__,
    description="Python client for the Digital Ocean API",
    long_description=read("README.rst"),
    author="devo.ps",
    author_email="vincent@devo.ps",
    maintainer="Vincent Viallet",
    maintainer_email="vincent@devo.ps",
    url="https://github.com/devo-ps/dopy",
    download_url="https://github.com/devo-ps/dopy/archive/master.zip",
    classifiers=("Development Status :: 3 - Alpha",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2.6",
                 "Programming Language :: Python :: 2.7"),
    license=read("LICENSE"),
    packages=['dopy'],
    install_requires=["requests >= 1.0.4"],
)