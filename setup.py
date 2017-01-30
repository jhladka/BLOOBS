#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README') as f:
    long_description = ''.join(f.readlines())

setup(
    name='bloobs',
    version='1.0',
    description='Easy shooting game',
    long_description=long_description,
    author='Jarmila Hladká',
    author_email='jarka.repakova@gmail.com',
    keywords='game',
    license='Public Domain',
    url='https://github.com/jhladka/BLOOBS',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment :: Arcade',
        ],
    packages=find_packages(exclude=['.git',]),
    package_data={
        '': ['*.py', '.highest_score.txt', 'PNG/*.png', 'SOUNDS/*.wav'],
        },
    install_requires=['pyglet'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'bloobs = bloobs.bloobs:main',
        ],
    },
)
