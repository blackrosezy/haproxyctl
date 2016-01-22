#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
        name='Haproxyctl',
        version='0.1.0',
        author='Mohd Rozi',
        author_email='blackrosezy@gmail.com',
        scripts=['bin/haproxyctl'],
        description='Haproxy reverse proxy cli',
        install_requires=[
            "Jinja2>=2.8",
            "docker-py>=1.6.0",
            "docopt>=0.6.2",
        ],
)
