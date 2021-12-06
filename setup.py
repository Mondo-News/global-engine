from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='global-engine',
    version='1.0.0',
    packages=[''],
    url='https://github.com/Mondo-News/global-engine',
    license='',
    author='Victor Möslein & Benedikt Ströbl',
    author_email='stroebl.benedikt@gmail.com',
    description='Your visual global news platform',
    install_requires=required
)