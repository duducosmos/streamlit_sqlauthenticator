#!/usr/bin/env python3
# -*- Coding: UTF-8 -*-
import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="streamlit_sqlauthenticator",
    license="Apache License 2.0",
    version='0.1.0',
    author='Eduardo S. Pereira',
    author_email='pereira.somoza@gmail.com',
    packages=find_packages("src"),
    package_dir={"": "src"},
    description="Basic Authenticator for Streamlit",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/duducosmos/streamlit_sqlauthenticator",
    install_requires=["pydal",
                      "bcrypt",
                      "streamlit",
                      ],

)