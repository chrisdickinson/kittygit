#!/usr/bin/python
from setuptools import setup, find_packages
import os

setup(
    name = "kittygit",
    version = "0.1",
    packages = find_packages(),

    author = "Chris Dickinson",
    author_email = "chris@neversaw.us",
    description = "nappingcat app for handling git calls over SSH",
    long_description = """
        An implementation of gitosis for the nappingcat framework.
""".strip(),
    license = "BSD / GPLv3 / CDDL",
    keywords = "framework restrict commands ssh git",
    url = "http://github.com/chrisdickinson/kittygit/",
    zip_safe=False,
    install_requires=[
        # setuptools 0.6a9 will have a non-executeable post-update
        # hook, this will make gitosis-admin settings not update
        # (fixed in 0.6c5, maybe earlier)
        'setuptools>=0.6c5',
        ],
    )


