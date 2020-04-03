#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

import pymfy

NAME = "pymfy"
HERE = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = "\n" + f.read()


setup(
    name=NAME,
    version=pymfy.__version__,
    description="A Somfy Open API library",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="ETIENNE Thibaut",
    python_requires=">=3.4",
    url="https://github.com/tetienne/somfy-open-api",
    packages=find_packages(exclude=("tests",)),
    install_requires=["requests-oauthlib", 'typing;python_version<"3.5"'],
    include_package_data=True,
    license="GNU General Public License v3.0",
)
