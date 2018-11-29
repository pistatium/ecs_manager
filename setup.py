# coding: utf-8

import os
import sys
from setuptools import setup, find_packages
from pip.req import parse_requirements

setup(
    name='ecs_manager',
    version='0.1.4.3',
    url='https://github.com/pistatium/ecs_service_manager',
    author='pistatium',
    description='Manage ecs service',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'click',
        'future'
    ],
    entry_points={
        'console_scripts': [
            'ecs_manager=ecs_manager.cmd:main'
        ]
    },
)

