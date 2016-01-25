#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
        name='Haproxyctl',
        version='0.1.0',
        author='Mohd Rozi',
        author_email='blackrosezy@gmail.com',
        packages=['haproxyctl'],
        description='Haproxy reverse proxy cli',
        url='http://morzproject.com',
        install_requires=[
            "Jinja2>=2.8",
            "docker-py>=1.6.0",
            "docopt>=0.6.2",
        ],
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'haproxyctl=haproxyctl.haproxyctl:main',
            ],
        },
)
