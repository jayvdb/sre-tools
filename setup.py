#!/usr/bin/env python
"""SRE regex tools."""

"""
Copyright 2020 John Vandenberg

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
    description="Tools for manupulating sre_parse data structures",
    license="Apache-2.0",
    author_email="jayvdb@gmail.com",
    url="https://github.com/jayvdb/sre-tools",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    classifiers=classifiers.splitlines(),
    tests_require=[],
)
