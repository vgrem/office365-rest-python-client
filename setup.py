#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io

from setuptools import find_packages, setup

with io.open("README.md", mode="r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="office365-rest-python-client",
    version="3.0.0.dev1",
    author="Vadim Gremyachev",
    author_email="vvgrem@gmail.com",
    maintainer="Domenico Di Nicola",
    maintainer_email="dom.dinicola@gmail.com",
    description="Microsoft 365 & Microsoft Graph Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vgrem/office365-rest-python-client",
    python_requires='>=3.6',
    install_requires=[
        "requests>=2.32.4,<3.0.0",
        "msal>=1.28.0,<2.0.0",
        "pytz>=2023.3",
        "typing_extensions>=4.5.0",
    ],
    extras_require={
        "NtlmProvider": ["requests_ntlm>=1.2.0"],
    },
    tests_require=[
        "pytest>=7.0.0",
        "adal>=1.2.7",
    ],
    test_suite="tests",
    license="MIT",
    keywords="git",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(
        exclude=[
            "tests",
            "tests.*",
            "generator",
            "generator.*",
            "examples",
            "examples.*",
        ]
    ),
    package_data={
        "office365": [
            "runtime/auth/providers/templates/SAML.xml",
            "runtime/auth/providers/templates/RST2.xml",
            "runtime/auth/providers/templates/FederatedSAML.xml",
        ]
    },
)
