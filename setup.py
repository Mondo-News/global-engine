"""
This module provides an easy way to set up this project on your local machine and will install all required dependencies
when called.
"""
from setuptools import setup

if __name__ == "__main__":
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    setup(
        name='Mondo News',
        version='0.1',
        url='https://github.com/Mondo-News/global-engine',
        license='',
        author='Victor Möslein & Benedikt Ströbl',
        author_email='stroebl.benedikt@gmail.com',
        description='Your visual global news platform',
        install_requires=required
    )