#!/usr/bin/env python
"""SRE regex tools."""

from setuptools import find_packages, setup

__version__ = "0.0.1"

classifiers = """\
Environment :: Console
Intended Audience :: Developers
Intended Audience :: Science/Research
Intended Audience :: System Administrators
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: Implementation :: CPython
Topic :: Security
Development Status :: 4 - Beta
"""

setup(
    name="sre-tools",
    version=__version__,
    description="Tools for manipulating sre_parse data structures",
    license="Apache-2.0",
    author_email="jayvdb@gmail.com",
    url="https://github.com/jayvdb/sre-tools",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    classifiers=classifiers.splitlines(),
    tests_require=[],
)
